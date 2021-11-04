import time
import helper
import logging
from telebot import types
from datetime import datetime


def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id
    history = helper.getUserHistory(chat_id)
    if history is None:
        bot.send_message(chat_id, "Oops! Looks like you do not have any spending records!")
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        for mode in helper.getSpendDisplayOptions():
            markup.add(mode)
        # markup.add('Day', 'Month')
        msg = bot.reply_to(message, 'Please select a category to see the total expense', reply_markup=markup)
        bot.register_next_step_handler(msg, display_total, bot)


def display_total(message, bot):
    try:
        chat_id = message.chat.id
        DayWeekMonth = message.text

        if DayWeekMonth not in helper.getSpendDisplayOptions():
            raise Exception("Sorry I can't show spendings for \"{}\"!".format(DayWeekMonth))

        history = helper.getUserHistory(chat_id)
        if history is None:
            raise Exception("Oops! Looks like you do not have any spending records!")

        bot.send_message(chat_id, "Hold on! Calculating...")
        # show the bot "typing" (max. 5 secs)
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(0.5)

        total_text = ""

        if DayWeekMonth == 'Day':
            query = datetime.now().today().strftime(helper.getDateFormat())
            # query all that contains today's date
            queryResult = [value for index, value in enumerate(history) if str(query) in value]
        elif DayWeekMonth == 'Month':
            query = datetime.now().today().strftime(helper.getMonthFormat())
            # query all that contains today's date
            queryResult = [value for index, value in enumerate(history) if str(query) in value]
        total_text = calculate_spendings(queryResult)

        spending_text = ""
        if len(total_text) == 0:
            spending_text = "You have no spendings for {}!".format(DayWeekMonth)
        else:
            spending_text = "Here are your total spendings {}:\nCATEGORIES,AMOUNT \n----------------------\n{}".format(DayWeekMonth.lower(), total_text)

        bot.send_message(chat_id, spending_text)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))


def calculate_spendings(queryResult):
    total_dict = {}

    for row in queryResult:
        # date,cat,money
        s = row.split(',')
        # cat
        cat = s[1]
        if cat in total_dict:
            # round up to 2 decimal
            total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
        else:
            total_dict[cat] = float(s[2])
    total_text = ""
    for key, value in total_dict.items():
        total_text += str(key) + " $" + str(value) + "\n"
    return total_text

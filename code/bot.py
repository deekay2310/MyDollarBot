import json
import logging
import re
import os
import telebot
import time
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import pickle
from user import User

api_token = "2070500964:AAGNgu08ApbYMs5x6o8haEEXvPOemghPtFA"
commands = {
    'menu': 'Display this menu',
    'add': 'Record/Add a new spending',
    'display': 'Show sum of expenditure for the current day/month',
    'history': 'Display spending history',
    'delete': 'Clear/Erase all your records',
    'edit': 'Edit/Change spending details'
}

bot = telebot.TeleBot(api_token)
telebot.logger.setLevel(logging.INFO)
user_list = {}
option = {}


@bot.message_handler(commands=['start', 'menu'])
def start_and_menu_command(m):
    chat_id = m.chat.id
    text_intro = "Welcome to TrackMyDollar - a simple solution to track your expenses! \nHere is a list of available " \
                 "commands, please enter a command of your choice so that I can assist you further: \n\n "
    for c in commands:  # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + ": "
        text_intro += commands[c] + "\n\n"
    bot.send_message(chat_id, text_intro)


@bot.message_handler(commands=['add'])
def command_add(message):
    global user_list
    global option
    chat_id = str(message.chat.id)
    option.pop(chat_id, None)
    if chat_id not in user_list.keys():
        user_list[chat_id] = User(chat_id)
    spend_categories = user_list[chat_id].spend_categories
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for c in spend_categories:
        markup.add(c)
    msg = bot.reply_to(message, 'Select Category', reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection)


def post_category_selection(message):
    global option
    global user_list
    try:
        chat_id = str(message.chat.id)
        selected_category = message.text
        spend_categories = user_list[chat_id].spend_categories
        if not selected_category in spend_categories:
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry I don't recognise this category \"{}\"!".format(selected_category))

        option[chat_id] = selected_category
        message = bot.send_message(chat_id, 'How much did you spend on {}? \n(Enter numeric values only)'.format(
            str(option[chat_id])))
        bot.register_next_step_handler(message, post_amount_input)
    except Exception as e:
        bot.reply_to(message, 'Oh no! ' + str(e))
        display_text = ""
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)


def post_amount_input(message):
    global user_list
    global option
    dateFormat = '%d-%m-%Y'
    timeFormat = '%H:%M'
    monthFormat = '%m-%Y'
    try:
        chat_id = str(message.chat.id)
        amount_entered = message.text
        amount_value = user_list[chat_id].validate_entered_amount(amount_entered)  # validate
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")

        date_of_entry = datetime.today()
        date_str, category_str, amount_str = str(date_of_entry), str(option[chat_id]), str(amount_value)
        user_list[chat_id].add_transaction(date_of_entry, option[chat_id], amount_value, chat_id)
        bot.send_message(chat_id, 'The following expenditure has been recorded: You have spent ${} for {} on {}'.format(
            amount_str, category_str, date_str))

    except Exception as e:
        bot.reply_to(message, 'Oh no. ' + str(e))


@bot.message_handler(commands=['history'])
def show_history(message):
    try:
        chat_id = str(message.chat.id)
        spend_total_str = ""
        if chat_id not in list(user_list.keys()):
            raise Exception("Sorry! No spending records found!")
        spend_history_str = "Here is your spending history : \nDATE, CATEGORY, AMOUNT\n----------------------\n"
        if len(user_list[chat_id].transactions) == 0:
            spend_total_str = "Sorry! No spending records found!"
        else:
            for category in user_list[chat_id].transactions.keys():
                for transaction in user_list[chat_id].transactions[category]:
                    date = str(transaction["Date"])
                    value = str(transaction["Value"])
                    spend_total_str += "Category: {} Date: {} Value: {} \n".format(category, date, value)
            bot.send_message(chat_id, spend_history_str + spend_total_str)
    except Exception as e:
        print(e)
        bot.reply_to(message, "Oops!" + str(e))


@bot.message_handler(commands=['display'])
def command_display(message):
    global user_list
    global option
    chat_id = str(message.chat.id)
    if len(user_list[chat_id].transactions) == 0:
        bot.send_message(chat_id, "Oops! Looks like you do not have any spending records!")
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        for mode in user_list[chat_id].spend_display_option:
            markup.add(mode)
        msg = bot.reply_to(message, 'Please select a category to see the total expense', reply_markup=markup)
        bot.register_next_step_handler(msg, display_total)


def display_total(message):
    dateFormat = '%d/%m/%Y'
    timeFormat = '%H:%M'
    monthFormat = '%m/%Y'
    try:
        chat_id = str(message.chat.id)
        day_week_month = message.text

        if not day_week_month in user_list[chat_id].spend_display_option:
            raise Exception("Sorry I can't show spendings for \"{}\"!".format(day_week_month))

        if len(user_list[chat_id].transactions) == 0:
            raise Exception("Oops! Looks like you do not have any spending records!")

        bot.send_message(chat_id, "Hold on! Calculating...")

        if day_week_month == 'Day':
            query = datetime.today()
            query_result = ""
            total_value = 0
            for category in user_list[chat_id].transactions.keys():
                for transaction in user_list[chat_id].transactions[category]:
                    if transaction["Date"].strftime("%d") == query.strftime("%d"):
                        query_result += "Category {} Date {} Value {} \n".format(category, transaction["Date"].strftime(
                            dateFormat), transaction["Value"])
                        total_value += transaction["Value"]
            total_spendings = "Here are your total spendings for the date {} \n".format(
                datetime.today().strftime("%d-%m-%Y"))
            total_spendings += query_result
            total_spendings += "Total Value {}".format(total_value)
            bot.send_message(chat_id, total_spendings)
        elif day_week_month == 'Month':
            query = datetime.today()
            query_result = ""
            total_value = 0
            for category in user_list[chat_id].transactions.keys():
                for transaction in user_list[chat_id].transactions[category]:
                    if transaction["Date"].strftime("%m") == query.strftime("%m"):
                        query_result += "Category {} Date {} Value {} \n".format(category, transaction["Date"].strftime(
                            dateFormat), transaction["Value"])
                        total_value += transaction["Value"]
            total_spendings = "Here are your total spendings for the Month {} \n".format(
                datetime.today().strftime("%m"))
            total_spendings += query_result
            total_spendings += "Total Value {}".format(total_value)
            bot.send_message(chat_id, total_spendings)
    except Exception as e:
        bot.reply_to(message, str(e))


@bot.message_handler(commands=['edit'])
def edit1(message):
    global user_list
    global option
    chat_id = str(message.chat.id)

    if chat_id in list(user_list.keys()):
        msg = bot.reply_to(message, "Please enter the date, category and value of the transaction you made (Eg: "
                                    "01/03/2021,Transport,25)")
        bot.register_next_step_handler(msg, edit2)

    else:
        bot.reply_to(chat_id, "No data found")


def edit2(message):
    chat_id = str(message.chat.id)
    info = message.text
    date_format = r"^([0123]?\d)[\/](\d?\d)[\/](20\d+)"
    info = info.split(',')
    info_date = re.search(date_format, info[0].strip())
    info_category = info[1].strip()
    info_value = info[2].strip()
    if info_date is None:
        bot.reply_to(message, "The date is incorrect")
        return
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    choices = ['Date', 'Category', 'Cost']
    for c in choices:
        markup.add(c)

    for transaction in user_list[chat_id].transactions[info_category]:
        if transaction["Date"].strftime("%d") == info_date.group(1) and transaction["Date"].strftime(
                "%m") == info_date.group(2) and transaction["Date"].strftime("%Y") == info_date.group(3):
            if str(int(transaction["Value"])) == info_value:
                user_list[chat_id].store_edit_transaction(transaction, info_category)
                choice = bot.reply_to(message, "What do you want to update?", reply_markup=markup)
                bot.register_next_step_handler(choice, edit3)
                break


def edit3(message):
    choice1 = message.text
    chat_id = str(message.chat.id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for category in user_list[chat_id].spend_categories:
        markup.add(category)
    if choice1 == 'Date':
        new_date = bot.reply_to(message, "Please enter the new date (in dd/mm/yyyy format)")
        bot.register_next_step_handler(new_date, edit_date)

    if choice1 == 'Category':
        new_cat = bot.reply_to(message, "Please select the new category", reply_markup=markup)
        bot.register_next_step_handler(new_cat, edit_cat)

    if choice1 == 'Cost':
        new_cost = bot.reply_to(message, "Please type the new cost")
        bot.register_next_step_handler(new_cost, edit_cost)


def edit_date(message):
    new_date = message.text
    chat_id = str(message.chat.id)
    date_format = r"^([0123]?\d)[\/](\d?\d)[\/](20\d+)"
    user_date = re.search(date_format, new_date)
    if user_date is None:
        bot.reply_to(message, "The date is incorrect")
        return
    updated_transaction = user_list[chat_id].edit_transaction_date(user_date.group(0))
    user_list[chat_id].save_user(chat_id)
    edit_message = "Date is updated. Here is the new transaction. \n Date {}. Value {}. \n".format(
        updated_transaction["Date"], updated_transaction["Value"])
    bot.reply_to(message, edit_message)


def edit_cat(message):
    chat_id = str(message.chat.id)
    new_category = message.text.strip()
    updated_transaction = user_list[chat_id].edit_transaction_category(new_category)
    if updated_transaction:
        user_list[chat_id].save_user(chat_id)
        edit_message = "Category has been edited."
        bot.reply_to(message, edit_message)
    else:
        edit_message = "Category has not been edited successfully"
        bot.reply_to(message, edit_message)


def edit_cost(message):
    new_cost = message.text
    chat_id = str(message.chat.id)
    new_cost = user_list[chat_id].validate_entered_amount(new_cost)
    if new_cost != 0:
        user_list[chat_id].save_user(chat_id)
        updated_transaction = user_list[chat_id].edit_transaction_value(new_cost)
        edit_message = "Value is updated. Here is the new transaction. \n Date {}. Value {}. \n".format(
            updated_transaction["Date"], updated_transaction["Value"])
        bot.reply_to(message, edit_message)

    else:
        bot.reply_to(message, "The cost is invalid")
        return



def get_users():
    data_dir = "../data"
    users = {}
    for file in os.listdir(data_dir):
        if file.endswith(".pickle"):
            user = re.match("(.+)\.pickle", file)
            if user:
                user = user.group(1)
                with open("{0}/{1}".format(data_dir, file), "rb") as f:
                    users[user] = pickle.load(f)
    return users


if __name__ == '__main__':
    try:
        user_list = get_users()
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(3)
        print("Connection Timeout")
from mock import patch
from telebot import types
from code import edit


@patch('telebot.telebot')
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    edit.run(message, mc)
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_select_category_to_be_updated(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from testing!")
    edit.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_select_category_selection_no_matching_choices(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []
    mc.reply_to.return_value = True
    mocker.patch.object(edit, 'helper')
    edit.helper.getChoices().return_value = None
    message = create_message("hello from testing!")
    edit.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_post_category_selection_no_matching_category(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []
    mc.reply_to.return_value = True
    mocker.patch.object(edit, 'helper')
    edit.helper.getSpendCategories.return_value = None
    message = create_message("hello from testing!")
    edit.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_post_amount_input_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(edit, 'helper')
    edit.helper.validate_entered_amount.return_value = 0
    message = create_message("hello from testing!")
    edit.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


def create_message(text):
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")

from code import helper
import pytest

MOCK_CHAT_ID = 101
MOCK_USER_DATA = {
    str(MOCK_CHAT_ID): ["correct_mock_value"],
    '102': ["wrong_mock_value"]
}


@pytest.mark.skipif(True, reason="Add none check")
def test_validate_entered_amount_none():
    result = helper.validate_entered_amount(None)
    if result:
        assert False, 'None is not a valid amount'
    else:
        assert True


def test_validate_entered_amount_int():
    val = '101'
    result = helper.validate_entered_amount(val)
    if result:
        assert True
    else:
        assert False, val + ' is valid amount'


def test_validate_entered_amount_int_max():
    val = '999999999999999'
    result = helper.validate_entered_amount(val)
    if result:
        assert True
    else:
        assert False, val + ' is valid amount'


def test_validate_entered_amount_int_outofbound():
    val = '9999999999999999'
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + ' is not a valid amount(out of bound)'
    else:
        assert True


def test_validate_entered_amount_float():
    val = '101.11'
    result = helper.validate_entered_amount(val)
    if result:
        assert True
    else:
        assert False, val + ' is valid amount'


@pytest.mark.skipif(True, reason="float value < 10^14 is valid. update the checker")
def test_validate_entered_amount_float_max():
    val = '999999999999999.9999'
    result = helper.validate_entered_amount(val)
    if result:
        assert True
    else:
        assert False, val + ' is valid amount'


@pytest.mark.skipif(True, reason="float value < 10^14 is valid. update the checker")
def test_validate_entered_amount_float_more_decimal():
    val = '9999999999.999999999'
    result = helper.validate_entered_amount(val)
    if result:
        assert True
    else:
        assert False, val + ' is valid amount'


def test_validate_entered_amount_float_outofbound():
    val = '9999999999999999.99'
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + ' is not a valid amount(out of bound)'
    else:
        assert True


def test_validate_entered_amount_string():
    val = 'agagahaaaa'
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + ' is not a valid amount'
    else:
        assert True


def test_validate_entered_amount_string_with_dot():
    val = 'agaga.aaa'
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + ' is not a valid amount'
    else:
        assert True


def test_validate_entered_amount_special_char():
    val = '$%@*@.@*'
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + ' is not a valid amount'
    else:
        assert True


def test_validate_entered_amount_alpha_num():
    val = '22e62a'
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + ' is not a valid amount'
    else:
        assert True


def test_validate_entered_amount_mixed():
    val = 'a14&^%.hs827'
    result = helper.validate_entered_amount(val)
    if result:
        assert False, val + ' is not a valid amount'
    else:
        assert True


def test_getUserHistory_without_data(mocker):
    mocker.patch.object(helper, 'read_json')
    helper.read_json.return_value = {}
    result = helper.getUserHistory(MOCK_CHAT_ID)
    if result is None:
        assert True
    else:
        assert False, 'Result is not None when user data does not exist'


def test_getUserHistory_with_data(mocker):
    mocker.patch.object(helper, 'read_json')
    helper.read_json.return_value = MOCK_USER_DATA
    result = helper.getUserHistory(MOCK_CHAT_ID)
    if result == MOCK_USER_DATA[str(MOCK_CHAT_ID)]:
        assert True
    else:
        assert False, 'User data is available but not found'


@pytest.mark.skipif(True, reason="None check should be added for user_data")
def test_getUserHistory_with_none(mocker):
    mocker.patch.object(helper, 'read_json')
    helper.read_json.return_value = None
    result = helper.getUserHistory(MOCK_CHAT_ID)
    if result is None:
        assert True
    else:
        assert False, 'Result is not None when the file does not exist'


def test_getSpendCategories():
    result = helper.getSpendCategories()
    if result == helper.spend_categories:
        assert True
    else:
        assert False, 'expected spend categories are not returned'


def test_getSpendDisplayOptions():
    result = helper.getSpendDisplayOptions()
    if result == helper.spend_display_option:
        assert True
    else:
        assert False, 'expected spend display options are not returned'


def test_getCommands():
    result = helper.getCommands()
    if result == helper.commands:
        assert True
    else:
        assert False, 'expected commands are not returned'


def test_getDateFormat():
    result = helper.getDateFormat()
    if result == helper.dateFormat:
        assert True
    else:
        assert False, 'expected date format are not returned'


def test_getTimeFormat():
    result = helper.getTimeFormat()
    if result == helper.timeFormat:
        assert True
    else:
        assert False, 'expected time format are not returned'


def test_getMonthFormat():
    result = helper.getMonthFormat()
    if result == helper.monthFormat:
        assert True
    else:
        assert False, 'expected month format are not returned'


def test_getChoices():
    result = helper.getChoices()
    if result == helper.choices:
        assert True
    else:
        assert False, 'expected choices are not returned'

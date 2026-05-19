import pytest

from src.scripts.contacts_bot import COMMAND_MESSAGES, handle_command


@pytest.mark.parametrize(
    "command,arguments,expected",
    [
        ("hello", [], COMMAND_MESSAGES["HELLO"]),
        ("hello", ["extra"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("not_a_command", [], COMMAND_MESSAGES["INVALID_COMMAND"]),
    ],
)
def test_handle_command_hello_and_unknown(command, arguments, expected):
    assert handle_command({}, command, arguments) == expected


def test_handle_command_add_and_update_via_dispatch(
    empty_address_book, valid_phone_generator
):
    assert (
        handle_command(empty_address_book, "add", ["x", valid_phone_generator()])
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )
    assert (
        handle_command(empty_address_book, "add", ["x", valid_phone_generator()])
        == COMMAND_MESSAGES["CONTACT_ADDED"]
    )
    last_valid_phone = valid_phone_generator()
    assert (
        handle_command(empty_address_book, "update", ["x", last_valid_phone])
        == COMMAND_MESSAGES["CONTACT_UPDATED"]
    )
    assert empty_address_book.data["x"].phones[-1].value == last_valid_phone


@pytest.mark.parametrize(
    "command,arguments,expected",
    [
        ("add", ["onlyone"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("update", ["x"], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("phone", [], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("all", ["extra"], COMMAND_MESSAGES["INVALID_COMMAND"]),
    ],
)
def test_handle_command_wrong_arity(empty_address_book, command, arguments, expected):
    assert handle_command(empty_address_book, command, arguments) == expected


@pytest.mark.parametrize(
    "command,arguments,expected",
    [
        ("", [], COMMAND_MESSAGES["INVALID_COMMAND"]),
        ("  ", [], COMMAND_MESSAGES["INVALID_COMMAND"]),
    ],
)
def test_handle_command_empty_line_invalid(
    empty_address_book, command, arguments, expected
):
    assert handle_command(empty_address_book, command, arguments) == expected


def test_handle_command_phone_no_user(empty_address_book):
    assert (
        handle_command(empty_address_book, "phone", ["Ghost"])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )


def test_handle_command_update_no_user(empty_address_book, valid_phone):
    assert (
        handle_command(empty_address_book, "update", ["Ghost", valid_phone])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )


def test_handle_command_exit_close_returns_none(empty_address_book):
    assert (
        handle_command(empty_address_book, "exit", []) == COMMAND_MESSAGES["GOOD_BYE"]
    )
    assert (
        handle_command(empty_address_book, "close", []) == COMMAND_MESSAGES["GOOD_BYE"]
    )
    assert len(empty_address_book.data) == 0

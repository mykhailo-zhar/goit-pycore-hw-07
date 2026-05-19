import pytest

from src.scripts.contacts_bot import COMMAND_MESSAGES, add_birthday

from .shared import RECORD_ERRORS

VALID_BIRTHDAY = "01.01.1990"
NEW_BIRTHDAY = "02.02.1991"
INVALID_BIRTHDAY = "31.02.1990"


def test_add_birthday_adds_to_existing_record(book_with_contact):
    assert add_birthday(
        book_with_contact, ["JohnDoe", VALID_BIRTHDAY]
    ) == COMMAND_MESSAGES["BIRTHDAY_ADDED"].format(
        old_birthday=None, new_birthday=VALID_BIRTHDAY, name="JohnDoe"
    )
    assert book_with_contact.data["JohnDoe"].birthday.value == VALID_BIRTHDAY


def test_add_birthday_edits_record_stored_in_address_book(book_with_contact):
    record = book_with_contact.data["JohnDoe"]

    assert add_birthday(
        book_with_contact, ["JohnDoe", VALID_BIRTHDAY]
    ) == COMMAND_MESSAGES["BIRTHDAY_ADDED"].format(
        old_birthday=None, new_birthday=VALID_BIRTHDAY, name="JohnDoe"
    )

    assert book_with_contact.data["JohnDoe"] is record
    assert record.birthday.value == VALID_BIRTHDAY


def test_add_birthday_no_such_user(empty_address_book):
    assert (
        add_birthday(empty_address_book, ["Nobody", VALID_BIRTHDAY])
        == COMMAND_MESSAGES["NO_SUCH_USER"]
    )
    assert len(empty_address_book.data) == 0


def test_add_birthday_invalid_birthday(book_with_contact):
    assert add_birthday(
        book_with_contact, ["JohnDoe", INVALID_BIRTHDAY]
    ) == RECORD_ERRORS["BIRTHDAY_NOT_VALID"].format(birthday=INVALID_BIRTHDAY)
    assert book_with_contact.data["JohnDoe"].birthday is None


def test_add_birthday_replaces_existing_birthday(book_with_contact):
    add_birthday(book_with_contact, ["JohnDoe", VALID_BIRTHDAY])

    assert add_birthday(
        book_with_contact, ["JohnDoe", NEW_BIRTHDAY]
    ) == COMMAND_MESSAGES["BIRTHDAY_ADDED"].format(
        old_birthday=VALID_BIRTHDAY, new_birthday=NEW_BIRTHDAY, name="JohnDoe"
    )
    assert book_with_contact.data["JohnDoe"].birthday.value == NEW_BIRTHDAY


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["JohnDoe"],
        ["JohnDoe", VALID_BIRTHDAY, NEW_BIRTHDAY],
    ],
)
def test_add_birthday_wrong_arity(book_with_contact, arguments):
    assert (
        add_birthday(book_with_contact, arguments)
        == COMMAND_MESSAGES["INVALID_COMMAND"]
    )

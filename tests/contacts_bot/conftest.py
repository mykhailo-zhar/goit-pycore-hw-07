from random import randint

import pytest

from src.address_book import AddressBook
from src.scripts.contacts_bot import add_contact


@pytest.fixture
def empty_address_book():
    return AddressBook()


@pytest.fixture
def valid_phone_generator():
    def generator():
        return "".join([str(randint(0, 9)) for _ in range(10)])

    return generator


@pytest.fixture
def valid_phone(valid_phone_generator):
    return valid_phone_generator()


@pytest.fixture
def book_with_contact(empty_address_book, valid_phone):
    add_contact(empty_address_book, ["JohnDoe", valid_phone])
    return empty_address_book

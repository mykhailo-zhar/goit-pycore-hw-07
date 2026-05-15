import pytest

from src.fields.phone import Phone
from src.record import Record


@pytest.fixture
def valid_name():
    return "John Doe"


@pytest.fixture
def invalid_name():
    return 10


@pytest.fixture
def valid_phone():
    return Phone("1234567890")


@pytest.fixture
def invalid_phone():
    return Phone("12345678901")


@pytest.fixture
def record(valid_name, valid_phone):
    rec = Record(valid_name)
    rec.add_phone(valid_phone.value)
    return rec


def test_record_init(valid_name, valid_phone):
    record = Record(valid_name)
    record.add_phone(valid_phone.value)
    assert record._name.value == valid_name
    assert valid_phone.value in [phone.value for phone in record._phones]


def test_record_init_invalid_name(invalid_name, valid_phone):
    with pytest.raises(ValueError):
        Record(invalid_name)


def test_record_add_same_phone(record, valid_phone):
    with pytest.raises(ValueError):
        record.add_phone(valid_phone.value)


def test_record_add_invalid_phone(record, invalid_phone):
    with pytest.raises(ValueError):
        record.add_phone(invalid_phone.value)


def test_record_remove_phone(record, valid_phone):
    record.remove_phone(valid_phone.value)
    assert valid_phone not in record._phones


def test_record_remove_non_existent_phone(record, valid_phone):
    record.remove_phone(valid_phone.value)
    with pytest.raises(ValueError):
        record.remove_phone(valid_phone.value)


def test_record_find_phone(record, valid_phone):
    assert record.find_phone(valid_phone.value).value == valid_phone.value


def test_record_find_non_existent_phone(record, invalid_phone):
    assert record.find_phone(invalid_phone.value) is None


def test_record_edit_phone(record, valid_phone):
    record.edit_phone(valid_phone.value, "1234567891")
    assert record.find_phone("1234567891").value == "1234567891"


def test_record_edit_non_existent_phone(record, valid_phone):
    record.remove_phone(valid_phone.value)
    with pytest.raises(ValueError):
        record.edit_phone(valid_phone.value, "1234567891")


def test_record_edit_invalid_phone(record, valid_phone, invalid_phone):
    with pytest.raises(ValueError):
        record.edit_phone(valid_phone.value, invalid_phone.value)

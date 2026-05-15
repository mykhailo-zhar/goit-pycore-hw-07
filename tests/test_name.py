from src.fields.field import Field
from src.fields.name import Name


def test_name_is_subclass_of_field():
    assert issubclass(Name, Field)


def test_name_init():
    name = Name("John Doe")
    assert name.value == "John Doe"


def test_name_str():
    name = Name("John Doe")
    assert str(name) == "John Doe"


def test_name_validate():
    assert Name("John Doe").validate()

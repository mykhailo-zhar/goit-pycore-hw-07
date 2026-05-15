from src.fields.field import Field


def test_field_init():
    field = Field("test")
    assert field.value == "test"


def test_field_str():
    field = Field("test")
    assert str(field) == "test"

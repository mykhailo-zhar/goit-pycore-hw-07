import pytest
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from tasks.task4 import get_upcoming_birthdays
import re

@pytest.fixture
def users() -> list[dict]:
  return [ {"name": f"John Doe {i}", "birthday": (datetime.now() + relativedelta(days=i, years=-25)).strftime("%Y.%m.%d")} for i in range(-3,8)]

# Validation of input parameters

def test_non_list_input_raises_type_error():
  with pytest.raises(TypeError):
      get_upcoming_birthdays(1)

def test_non_list_dict_raises_value_error():
  with pytest.raises(ValueError):
      get_upcoming_birthdays([1,1,3])

@pytest.mark.parametrize('user_list', [
    [{}],
    [{"none": "none"}],
    [{"name": "John Doe"}],
    [{"birthday": "1985.01.23"}],
])
def test_list_with_absent_keys_raises_value_error(user_list):
  with pytest.raises(ValueError):
      get_upcoming_birthdays(user_list)


def test_empty_list_returns_empty_list():
  assert get_upcoming_birthdays([]) == []


def _is_valid_user(user: dict) -> bool:
  return isinstance(user, dict) \
          and "name" in user \
          and "congratulation_date" in user

def test_valid_input_returns_list_of_dictionaries(users):
  result = get_upcoming_birthdays(users)
  assert all(_is_valid_user(user) for user in result)

def test_each_date_is_in_valid_format(users):
  result = get_upcoming_birthdays(users)
  assert all(re.match(r"\d{4}\.\d{2}\.\d{2}", user["congratulation_date"]) for user in result)

# Logic

def _is_congratulation_date_in_next_7_days(user: dict) -> bool:
  date = datetime.strptime(user["congratulation_date"], "%Y.%m.%d")
  today = datetime.now()
  return date >= today and date < (today + timedelta(days=7))

def test_congratulation_date_is_in_next_7_days(users):
   
  result = get_upcoming_birthdays(users)
  assert all(_is_congratulation_date_in_next_7_days(user) for user in result)

def _is_congratulation_date_not_on_weekend(user: dict) -> bool:
  return datetime.strptime(user["congratulation_date"], "%Y.%m.%d").weekday() not in [5, 6]

def test_congratulation_date_is_not_on_weekend(users):
  result = get_upcoming_birthdays(users)
  assert all(_is_congratulation_date_not_on_weekend(user) for user in result)
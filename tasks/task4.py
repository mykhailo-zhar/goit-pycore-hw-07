from datetime import datetime, timedelta

def _validate_user_dict(user: dict) -> bool:
    return isinstance(user, dict) \
           and "name" in user \
           and "birthday" in user

def _parse_dates(users: list[dict]) -> list[dict]:
    return [_parse_user(user) for user in users]

def _parse_user(user: dict) -> dict:
    parsed_user = dict(
        user, 
        congratulation_date=_transform_birthday_to_congratulation_date(user["birthday"])
    )
    parsed_user.pop("birthday")
    return parsed_user

def _transform_birthday_to_congratulation_date(birthday: str) -> datetime:
    global today
    birthday_date = datetime.strptime(birthday, "%Y.%m.%d")
    congratulation_date = birthday_date.replace(year=today.year)
    weekday = congratulation_date.weekday()
    if weekday in [5, 6]:
        congratulation_date = congratulation_date + timedelta(days=7 - weekday)
    return congratulation_date
 
def _get_congratulated_users(users: list[dict]) -> list[dict]:
    global today
    upcoming_birthdays = []
    for user in users:
        if user["congratulation_date"] < today \
                or user["congratulation_date"] >= (today + timedelta(days=7)):
            continue
        parsed_user = user.copy()
        parsed_user.update(
            congratulation_date=user["congratulation_date"].strftime("%Y.%m.%d")
        )
        upcoming_birthdays.append(parsed_user)

    return upcoming_birthdays

def get_upcoming_birthdays(users: list[dict]) -> list[dict]:
    """
    Get the upcoming birthdays for the users.

    Args:
        users: The list of users.
    """
    if not users:
        return []
    
    if not all(_validate_user_dict(user) for user in users):
        raise ValueError(
            "Users must be a list of dictionaries with 'name' and 'birthday' keys"
        )

    global today
    today = datetime.now()

    parsed_users = _parse_dates(users)
    return _get_congratulated_users(parsed_users)
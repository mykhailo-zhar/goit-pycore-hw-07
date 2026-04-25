from datetime import datetime, timedelta

def _validate_user_dict(user: dict) -> bool:
    """
    Validate the user dictionary.

    Args:
        user: The user dictionary to validate.

    Returns:
        True if the user dictionary is valid, False otherwise.
    """
    return isinstance(user, dict) \
           and "name" in user \
           and "birthday" in user

def _parse_users_birthdates(users: list[dict]) -> list[dict]:
    """
    Parse the users' birthdays to the congratulation dates.

    Args:
        users: The list of users.

    Returns:
        The list of parsed users.
    """
    return [_parse_user_birthdate(user) for user in users]

def _parse_user_birthdate(user: dict) -> dict:
    """
    Parse the user's birthday to the congratulation date.

    Args:
        user: The user to parse.

    Returns:
        The parsed user.
    """
    parsed_user = dict(
        user, 
        congratulation_date=_transform_birthday_to_congratulation_date(user["birthday"])
    )

    # Remove irrelevant birthday key
    parsed_user.pop("birthday")
    return parsed_user

def _transform_birthday_to_congratulation_date(birthday: str) -> datetime:
    """
    Transform the birthday to the congratulation date.

    Args:
        birthday: The birthday of the user.

    Returns:
        The congratulation date.
    """
    global today
    birthday_date = datetime.strptime(birthday, "%Y.%m.%d")
    congratulation_date = birthday_date.replace(year=today.year)

    weekday = congratulation_date.weekday()

    # Move the congratulation date to the next Monday if it's on a weekend
    if weekday in [5, 6]:
        congratulation_date = congratulation_date + timedelta(days=7 - weekday)

    return congratulation_date
 
def _get_congratulated_users(parsed_users: list[dict]) -> list[dict]:
    """
    Present the users who need to be congratulated in the next 7 days.

    Args:
        parsed_users: The list of parsed users.

    Returns:
        The list of upcoming birthdays.
    """
    global today
    upcoming_birthdays = []
    for user in parsed_users:
        # Skip users whose congratulation date is not in the next 7 days
        if user["congratulation_date"] < today \
                or user["congratulation_date"] >= (today + timedelta(days=7)):
            continue

        # Update the congratulation date to the format 'YYYY.MM.DD'
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

    Raises:
        ValueError: If the users are not a list of dictionaries with 'name' and 'birthday' keys.

    Returns:
        The list of upcoming birthdays.
    """
    if not users:
        return []
    
    if any(not _validate_user_dict(user) for user in users):
        raise ValueError(
            "Users must be a list of dictionaries with 'name' and 'birthday' keys"
        )

    global today
    today = datetime.now()

    parsed_users = _parse_users_birthdates(users)
    return _get_congratulated_users(parsed_users)
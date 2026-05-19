import sys
from pathlib import Path

from src.record import Record

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).parent[3].absolute()))


from src.address_book import AddressBook

COMMAND_MESSAGES = {
    "INVALID_COMMAND": "Invalid command.",
    "CONTACT_ADDED": "Contact added.",
    "CONTACT_UPDATED": "Contact updated.",
    "NO_SUCH_USER": "No such user",
    "PLEASE_CHANGE_USER": "Please change the user",
    "GOOD_BYE": "Good bye!",
    "NO_USERS": "There are no users",
    "HELLO": "How can I help you?",
}


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, IndexError) as e:
            return str(e)

    return wrapper


def parse_input(line: str) -> tuple[str, list[str]]:
    """
    Parse the input.

    Args:
        line (str): The line to parse.

    Returns:
        tuple[str, list[str]]: A tuple containing the command and the arguments.
    """
    if line.strip() == "":
        return "", []
    arguments = line.split()
    return arguments[0].lower(), arguments[1:]


@input_error
def hello(arguments: list[str] = []) -> str:
    """
    Print the hello message.

    Args:
        arguments (list[str]): The arguments to the hello command.

    Returns:
        str: The hello message.
    """
    if arguments:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])

    return COMMAND_MESSAGES["HELLO"]


@input_error
def add_contact(book: AddressBook, arguments: list[str]) -> str:
    """
    Add a new contact.

    Args:
        book (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to add the contact.

    Returns:
        str: The response to the command.
    """
    if len(arguments) < 2:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    name, *phones = arguments
    record = Record(name)
    for phone in phones:
        record.add_phone(phone)
    if book.find_record(name):
        raise ValueError(COMMAND_MESSAGES["PLEASE_CHANGE_USER"])
    book.add_record(record)
    return COMMAND_MESSAGES["CONTACT_ADDED"]


@input_error
def update_contact(book: AddressBook, arguments: list[str]) -> str:
    """
    Update a contact.

    Args:
        book (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to update the contact.

    Returns:
        str: The response to the command.
    """
    if len(arguments) < 2:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    name, *phones = arguments
    record = Record(name)
    for phone in phones:
        record.add_phone(phone)

    if not book.remove_record(name):
        raise ValueError(COMMAND_MESSAGES["NO_SUCH_USER"])

    book.add_record(record)

    return COMMAND_MESSAGES["CONTACT_UPDATED"]


@input_error
def show_phone(book: AddressBook, arguments: list[str]) -> str:
    """
    Show the phone number of a contact.

    Args:
        book (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to show the phone number of the contact.

    Returns:
        str: The response to the command.
    """
    if len(arguments) != 1:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    name = arguments[0]
    record = book.find_record(name)
    if not record:
        raise ValueError(COMMAND_MESSAGES["NO_SUCH_USER"])
    return "; ".join(phone.value for phone in record.phones)


@input_error
def show_all(book: AddressBook, arguments: list[str] = []) -> str:
    """
    Show all contacts.

    Args:
        book (AddressBook): The book of contacts.
        arguments (list[str]): The arguments to show all contacts.

    Returns:
        str: The response to the command.
    """
    if arguments:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    if not book.data:
        raise ValueError(COMMAND_MESSAGES["NO_USERS"])

    count_users = len(book.data)
    users_list = [
        f"{record.name}: {'; '.join(phone.value for phone in record.phones)}"
        for _, record in sorted(book.data.items())
    ]
    return f"Stored users ({count_users}):\n{'\n'.join(users_list)}"


@input_error
def exit(arguments: list[str] = []) -> str:
    """
    Exit the program.

    Args:
        arguments (list[str], optional): The arguments to the exit command. Defaults to [].

    Returns:
        str: The goodbye message.
    """
    if arguments:
        raise ValueError(COMMAND_MESSAGES["INVALID_COMMAND"])
    return COMMAND_MESSAGES["GOOD_BYE"]


def handle_command(book: AddressBook, command: str, arguments: list[str]) -> str:
    """
    Handle the command.

    Args:
        command (str): The command to handle.
        arguments (list[str]): The arguments to the command.
        book (AddressBook): The book of contacts.

    Returns:
        str: The response to the command.
    """

    match command:
        case "hello":
            return hello(arguments)
        case "add":
            return add_contact(book, arguments)
        case "update":
            return update_contact(book, arguments)
        case "phone":
            return show_phone(book, arguments)
        case "all":
            return show_all(book, arguments)
        case "exit":
            return exit(arguments)
        case "close":
            return exit(arguments)
        case _:
            return COMMAND_MESSAGES["INVALID_COMMAND"]


def main() -> None:
    """
    Main function.
    """
    book: AddressBook = AddressBook()
    while True:
        line = input()
        command, arguments = parse_input(line)
        response = handle_command(book, command, arguments)
        print(response)
        if command in ["exit", "close"]:
            break


if __name__ == "__main__":
    main()

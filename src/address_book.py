from src.record import Record


class AddressBook:
    def __init__(self):
        """
        Initialize the address book.
        """
        self.data = {}

    def add_record(self, record: Record):
        """
        Add a record to the address book.

        Args:
            record (Record): The record to add.
        """
        self.data[record.name.value] = record

    def find_record(self, name: str) -> Record | None:
        """
        Find a record in the address book.

        Args:
            name (str): The name of the record to find.

        Returns:
            Record | None: The record if found, None otherwise.
        """
        return self.data.get(name)

    def remove_record(self, name: str) -> bool:
        """
        Remove a record from the address book.

        Args:
            name (str): The name of the record to remove.

        Returns:
            bool: True if the record was removed, False otherwise.
        """

        return self.data.pop(name, None) is not None

    def get_upcoming_birthdays(self) -> list[Record]:
        """
        Get the upcoming birthdays from the address book.

        Returns:
            list[Record]: The upcoming birthdays.
        """
        raise NotImplementedError()

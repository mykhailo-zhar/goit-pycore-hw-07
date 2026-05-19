from dataclasses import dataclass
from datetime import datetime, timedelta

from src.fields.birthday import Birthday
from src.record import Record


@dataclass(init=False)
class ProcessedRecord:
    record: Record
    congratulation_date: datetime

    def __init__(self, record: Record, today: datetime):
        self.__record = record
        self.__today = today
        self.__congratulation_date = self.__calculate_congratulation_date()

    @property
    def record(self) -> Record:
        return self.__record

    @record.setter
    def record(self, record: Record):
        self.__record = record
        self.__congratulation_date = self.__calculate_congratulation_date()

    @property
    def congratulation_date(self) -> datetime:
        return self.__congratulation_date

    @staticmethod
    def is_congratulation_date_in_next_7_days(
        today: datetime,
    ):
        return lambda record: (
            record.congratulation_date >= today
            and record.congratulation_date < (today + timedelta(days=7))
        )

    def __calculate_congratulation_date(self) -> datetime:
        """
        Transform the birthday to the congratulation date.

        Args:
            birthday: The birthday of the user.

        Returns:
            The congratulation date.
        """
        birthday_date = datetime.strptime(
            self.record.birthday.value, Birthday.DATE_FORMAT
        )
        congratulation_date = birthday_date.replace(year=self.__today.year)

        weekday = congratulation_date.weekday()

        # Move the congratulation date to the next Monday if it's on a weekend
        if weekday in [5, 6]:
            congratulation_date = congratulation_date + timedelta(days=7 - weekday)

        return congratulation_date

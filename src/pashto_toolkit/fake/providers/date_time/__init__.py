"""Base date/time provider, using the Afghan solar calendar month names."""

from datetime import date, datetime, timedelta
from typing import Sequence, Union

from ...core import BaseProvider, date_between, datetime_between

DateLike = Union[date, datetime]


class Provider(BaseProvider):
    """Dates and times, with locale month and weekday names.

    ``month_names`` is indexed by calendar month, so slot 0 is unused and
    slots 1..12 hold the names. ``day_names`` starts on Saturday, which is
    how the Afghan week runs.
    """

    day_names: Sequence[str] = ()
    month_names: Sequence[str] = ()

    #: Oldest birth date date_of_birth() will produce, in years.
    max_age = 115

    # --- primitives -------------------------------------------------------
    def unix_time(self, start: int = 0, end: int = 2_000_000_000) -> int:
        return self.random_int(start, end)

    def date_object(self, start_year: int = 1970, end_year: int = 2035) -> date:
        return date_between(self.generator.random, date(start_year, 1, 1), date(end_year, 12, 31))

    def date_time(self, start_year: int = 1970, end_year: int = 2035) -> datetime:
        return datetime_between(
            self.generator.random, datetime(start_year, 1, 1), datetime(end_year, 12, 31, 23, 59, 59)
        )

    def date(self, pattern: str = "%Y-%m-%d") -> str:
        return self.date_object().strftime(pattern)

    def time(self, pattern: str = "%H:%M:%S") -> str:
        return self.date_time().strftime(pattern)

    # --- ranges -----------------------------------------------------------
    def date_between_dates(self, date_start: DateLike, date_end: DateLike) -> date:
        """A date in ``[date_start, date_end]``; the order may be reversed."""
        start = date_start.date() if isinstance(date_start, datetime) else date_start
        end = date_end.date() if isinstance(date_end, datetime) else date_end
        return date_between(self.generator.random, start, end)

    def date_between(self, start_date: DateLike, end_date: DateLike) -> date:
        return self.date_between_dates(start_date, end_date)

    def date_this_year(self) -> date:
        today = date.today()
        return date_between(self.generator.random, date(today.year, 1, 1), today)

    def date_this_decade(self) -> date:
        today = date.today()
        return date_between(self.generator.random, date(today.year - today.year % 10, 1, 1), today)

    def past_date(self, days: int = 30) -> date:
        today = date.today()
        return date_between(self.generator.random, today - timedelta(days=days), today)

    def future_date(self, days: int = 30) -> date:
        today = date.today()
        return date_between(self.generator.random, today, today + timedelta(days=days))

    def date_of_birth(self, minimum_age: int = 0, maximum_age: int = 115) -> date:
        """A birth date for somebody between the two ages, inclusive."""
        if minimum_age < 0 or maximum_age < 0:
            raise ValueError("ages cannot be negative")
        if minimum_age > maximum_age:
            raise ValueError("minimum_age cannot exceed maximum_age")
        today = date.today()
        youngest = today - timedelta(days=minimum_age * 365.25)
        oldest = today - timedelta(days=(maximum_age + 1) * 365.25 - 1)
        return date_between(self.generator.random, oldest, youngest)

    # --- parts ------------------------------------------------------------
    def year(self) -> str:
        return str(self.date_object().year)

    def month(self) -> str:
        return f"{self.date_object().month:02d}"

    def day_of_month(self) -> str:
        return f"{self.date_object().day:02d}"

    def month_name(self) -> str:
        """The locale month name for a random date."""
        return self.month_names[self.date_object().month]

    def day_of_week(self) -> str:
        """The locale weekday name, with the week starting on Saturday."""
        # date.weekday() is 0 for Monday; shift so Saturday lands on 0.
        return self.day_names[(self.date_object().weekday() + 2) % 7]

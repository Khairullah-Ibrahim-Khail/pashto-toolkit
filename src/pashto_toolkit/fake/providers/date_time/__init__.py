"""Base date/time provider, using the Afghan solar calendar month names."""

from datetime import date, datetime, timedelta
from datetime import time as _time
from datetime import timezone as _timezone
from typing import Optional, Sequence, Union

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

    #: IANA zones, led by Afghanistan's and those of its neighbours.
    timezones: Sequence[str] = (
        "Asia/Kabul", "Asia/Karachi", "Asia/Tehran", "Asia/Dushanbe", "Asia/Tashkent",
        "Asia/Ashgabat", "Asia/Kolkata", "Asia/Dubai", "Asia/Riyadh", "Europe/Istanbul",
        "Europe/London", "Europe/Berlin", "America/New_York", "America/Los_Angeles",
        "Asia/Shanghai", "Asia/Tokyo", "Australia/Sydney", "UTC",
    )

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

    # --- datetimes ------------------------------------------------------
    def date_time_between(self, start_date: DateLike, end_date: DateLike) -> datetime:
        """A datetime in ``[start_date, end_date]``."""
        start = start_date if isinstance(start_date, datetime) else datetime.combine(start_date, _time.min)
        end = end_date if isinstance(end_date, datetime) else datetime.combine(end_date, _time.max)
        return datetime_between(self.generator.random, start, end)

    def date_time_between_dates(self, datetime_start: DateLike, datetime_end: DateLike) -> datetime:
        return self.date_time_between(datetime_start, datetime_end)

    def date_time_this_year(self) -> datetime:
        now = datetime.now()
        return datetime_between(self.generator.random, datetime(now.year, 1, 1), now)

    def date_time_this_decade(self) -> datetime:
        now = datetime.now()
        return datetime_between(self.generator.random, datetime(now.year - now.year % 10, 1, 1), now)

    def date_time_this_month(self) -> datetime:
        now = datetime.now()
        return datetime_between(self.generator.random, datetime(now.year, now.month, 1), now)

    def past_datetime(self, days: int = 30) -> datetime:
        now = datetime.now()
        return datetime_between(self.generator.random, now - timedelta(days=days), now)

    def future_datetime(self, days: int = 30) -> datetime:
        now = datetime.now()
        return datetime_between(self.generator.random, now, now + timedelta(days=days))

    def date_this_month(self) -> date:
        today = date.today()
        return date_between(self.generator.random, date(today.year, today.month, 1), today)

    # --- times and offsets ----------------------------------------------
    def time_object(self) -> _time:
        return _time(self.random_int(0, 23), self.random_int(0, 59), self.random_int(0, 59))

    def time_delta(self, end_datetime: Optional[datetime] = None) -> timedelta:
        """A duration between zero and the distance to ``end_datetime``."""
        limit = int((end_datetime - datetime.now()).total_seconds()) if end_datetime else 365 * 24 * 3600
        return timedelta(seconds=self.random_int(0, abs(limit)))

    def iso8601(self) -> str:
        return self.date_time().isoformat()

    def am_pm(self) -> str:
        return self.random_element(("AM", "PM"))

    def century(self) -> str:
        return self.random_element(
            ("XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI")
        )

    def timezone(self) -> str:
        """An IANA zone name; Afghanistan's own comes first in the list."""
        return self.random_element(self.timezones)

    def utc_offset(self) -> str:
        """Afghanistan runs at UTC+04:30, which is one of the few half-hour-plus offsets."""
        return "+04:30"

    def tzinfo(self) -> _timezone:
        return _timezone(timedelta(minutes=270), name="Asia/Kabul")

    def unix_timestamp(self) -> int:
        return int(self.date_time().timestamp())

    def date_this_century(self) -> date:
        today = date.today()
        return date_between(self.generator.random, date(today.year - today.year % 100, 1, 1), today)

    def date_time_this_century(self) -> datetime:
        now = datetime.now()
        return datetime_between(self.generator.random, datetime(now.year - now.year % 100, 1, 1), now)

    def date_time_ad(self, start_year: int = 1) -> datetime:
        """A datetime anywhere from year ``start_year`` to now."""
        now = datetime.now()
        return datetime_between(self.generator.random, datetime(max(1, start_year), 1, 1), now)

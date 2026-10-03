"""Base job provider."""

from typing import Sequence

from ...core import BaseProvider


class Provider(BaseProvider):
    """Occupations from the locale's list."""

    jobs: Sequence[str] = ()

    def job(self) -> str:
        return self.random_element(self.jobs)

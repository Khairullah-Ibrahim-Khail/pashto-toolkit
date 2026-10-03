"""Base national-identifier provider."""

from ...core import BaseProvider


class Provider(BaseProvider):
    """The locale supplies its own national identifier format."""

    def ssn(self) -> str:
        return self.numerify("###-##-####")

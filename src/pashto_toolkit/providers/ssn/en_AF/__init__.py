from faker.providers.ssn import Provider as BaseProvider
from faker.utils import checksums


class Provider(BaseProvider):
    """Afghan national ID (tazkira) number.

    Format ``XXXX-XXX-XXX-XXX``: twelve random digits followed by a Luhn check
    digit, e.g. ``2222-323-423-432``.
    """

    #: Twelve base digits. The thirteenth is the Luhn check digit, so the
    #: pattern is eleven ``#`` after the leading non-zero ``%``.
    afghan_id_formats = ("%###########",)

    def afghan_id(self, separator: str = "-") -> str:
        """Generate an Afghan national ID with a valid Luhn check digit.

        :param separator: inserted between groups; pass ``""`` for bare digits.
        """
        base = self.numerify(self.random_element(self.afghan_id_formats))
        full = f"{base}{checksums.calculate_luhn(base)}"
        return separator.join((full[0:4], full[4:7], full[7:10], full[10:13]))

    def ssn(self, separator: str = "-") -> str:
        """Faker's standard formatter name for :meth:`afghan_id`."""
        return self.afghan_id(separator)

"""Whole-person records, assembled from the other providers."""

from typing import Any, Dict, Optional, Sequence

from ...core import BaseProvider
from ...types import SexLiteral


class Provider(BaseProvider):
    """One consistent record per call: the name matches the gender asked for."""

    #: Keys a full profile carries, in order.
    PROFILE_FIELDS: Sequence[str] = (
        "job", "company", "ssn", "residence", "blood_group", "website",
        "username", "name", "sex", "address", "mail", "birthdate",
    )
    SIMPLE_FIELDS: Sequence[str] = ("username", "name", "sex", "address", "mail", "birthdate")

    blood_groups: Sequence[str] = ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-")

    def blood_group(self) -> str:
        return self.random_element(self.blood_groups)

    def _sex(self, sex: Optional[SexLiteral]) -> SexLiteral:
        return sex if sex in ("M", "F") else self.random_element(("M", "F"))

    def _name_for(self, sex: SexLiteral) -> str:
        return self.generator.format("name_male" if sex == "M" else "name_female")

    def _identity(self, sex: SexLiteral) -> Dict[str, Any]:
        """A name with a username and address derived from it.

        One record describes one person, so the username and mail are built
        from the name rather than drawn separately. In ``pa_AF`` the display
        name is in Pashto script and cannot be transliterated here, so the
        username falls back to the Latin pools; it still matches the mail.
        """
        name = self._name_for(sex)
        # pass the gender too, so the fallback pool matches when the display
        # name cannot be transliterated
        username = self.generator.format("user_name", sex, name)
        domain = self.generator.format("free_email_domain")
        return {"name": name, "username": username, "mail": f"{username}@{domain}"}

    def simple_profile(self, sex: Optional[SexLiteral] = None) -> Dict[str, Any]:
        """A small record: username, name, sex, address, mail, birthdate."""
        chosen = self._sex(sex)
        identity = self._identity(chosen)
        return {
            "username": identity["username"],
            "name": identity["name"],
            "sex": chosen,
            "address": self.generator.format("address"),
            "mail": identity["mail"],
            "birthdate": self.generator.format("date_of_birth"),
        }

    def profile(self, fields: Optional[Sequence[str]] = None, sex: Optional[SexLiteral] = None) -> Dict[str, Any]:
        """A full record. ``fields`` selects a subset, in the order given."""
        chosen = self._sex(sex)
        identity = self._identity(chosen)
        record: Dict[str, Any] = {
            "job": self.generator.format("job"),
            "company": self.generator.format("company"),
            "ssn": self.generator.format("afghan_id"),
            "residence": self.generator.format("address"),
            "blood_group": self.blood_group(),
            "website": [self.generator.format("url") for _ in range(self.random_int(1, 3))],
            "username": identity["username"],
            "name": identity["name"],
            "sex": chosen,
            "address": self.generator.format("address"),
            "mail": identity["mail"],
            "birthdate": self.generator.format("date_of_birth"),
        }
        if fields is None:
            return record
        unknown = [field for field in fields if field not in record]
        if unknown:
            raise ValueError(f"Unknown profile fields {unknown}. Known: {sorted(record)}")
        return {field: record[field] for field in fields}

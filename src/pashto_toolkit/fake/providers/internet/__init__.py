"""Base internet provider: usernames, domains, emails, addresses."""

import random as _std_random
import re
from typing import List, Optional, Sequence

from ...core import BaseProvider

_NON_ASCII = re.compile(r"[^a-z0-9]+")


class Provider(BaseProvider):
    """Machine-readable network values.

    These stay in Latin script in both locales, because that is what domain
    names, email addresses and MAC addresses are in practice.
    """

    tlds: Sequence[str] = ("com", "net", "org", "af")
    safe_email_tlds: Sequence[str] = ("com", "net", "org")
    free_email_domains: Sequence[str] = ("gmail.com", "yahoo.com", "outlook.com")
    user_name_formats: Sequence[str] = (
        "{{last_name}}.{{first_name}}",
        "{{first_name}}.{{last_name}}",
        "{{first_name}}##",
        "?{{last_name}}",
    )
    email_formats: Sequence[str] = ("{{user_name}}@{{domain_name}}", "{{user_name}}@{{free_email_domain}}")
    url_formats: Sequence[str] = ("https://www.{{domain_name}}/", "https://{{domain_name}}/")
    uri_paths: Sequence[str] = ("", "about", "search", "posts", "category", "tag", "blog", "news")
    uri_pages: Sequence[str] = ("index", "home", "search", "main", "post", "register", "login", "about")
    uri_extensions: Sequence[str] = (".html", ".htm", ".php", ".jsp", ".asp", "")

    #: ASCII words for domains, slugs and file names. Domain names cannot
    #: carry Pashto script, so slugging Pashto words would leave nothing.
    slug_words: Sequence[str] = (
        "kabul", "herat", "kandahar", "mazar", "jalalabad", "kunduz", "ghazni",
        "bamyan", "pamir", "hindukush", "panjshir", "helmand", "amu", "kabulriver",
        "lapis", "saffron", "pomegranate", "almond", "pistachio", "carpet",
        "silk", "caravan", "bazaar", "qala", "minar", "darya", "kotal", "dasht",
        "spin", "tor", "shams", "nur", "sabz", "zarin", "watan", "pashto",
        "afghan", "aryana", "khyber", "zabul", "logar", "wardak", "nangarhar",
        "data", "cloud", "net", "soft", "tech", "media", "press", "post",
    )

    # --- slugs and domains ------------------------------------------------
    def slugify(self, value: str) -> str:
        """Lowercase ASCII slug; non-Latin text is dropped, so callers should
        pass transliterated input."""
        return _NON_ASCII.sub("-", value.lower()).strip("-")

    def tld(self) -> str:
        return self.random_element(self.tlds)

    def domain_word(self) -> str:
        return self.random_element(self.slug_words)

    def domain_name(self, levels: int = 1) -> str:
        if levels < 1:
            raise ValueError("levels must be at least 1")
        name = f"{self.domain_word()}.{self.tld()}"
        for _ in range(levels - 1):
            name = f"{self.domain_word()}.{name}"
        return name

    def free_email_domain(self) -> str:
        return self.random_element(self.free_email_domains)

    def hostname(self, levels: int = 1) -> str:
        host = self.random_element(("web", "srv", "mail", "db", "api", "lb"))
        return f"{host}-{self.random_int(1, 99):02d}.{self.domain_name(levels)}"

    # --- identities -------------------------------------------------------
    def user_name(self) -> str:
        name = self.slugify(self.bothify(self.parse(self.random_element(self.user_name_formats))))
        return name or self.lexify("??????", letters="abcdefghijklmnopqrstuvwxyz")

    def email(self) -> str:
        return self.parse(self.random_element(self.email_formats))

    def safe_email(self) -> str:
        return f"{self.user_name()}@example.{self.random_element(self.safe_email_tlds)}"

    def free_email(self) -> str:
        return f"{self.user_name()}@{self.free_email_domain()}"

    def company_email(self) -> str:
        return f"{self.user_name()}@{self.domain_name()}"

    # --- locations --------------------------------------------------------
    def uri_path(self, deep: int = 1) -> str:
        return "/".join(self.random_elements(self.uri_paths, length=max(1, deep)))

    def uri_page(self) -> str:
        return self.random_element(self.uri_pages)

    def uri_extension(self) -> str:
        return self.random_element(self.uri_extensions)

    def uri(self) -> str:
        return f"https://{self.domain_name()}/{self.uri_path()}/{self.uri_page()}{self.uri_extension()}"

    def url(self, schemes: Sequence[str] = ("http", "https")) -> str:
        return f"{self.random_element(schemes)}://{self.domain_name()}/"

    def slug(self, value_count: int = 3) -> str:
        """A hyphenated ASCII slug, suitable for URLs and file names."""
        return "-".join(self.random_elements(self.slug_words, length=max(1, value_count)))

    # --- network numbers --------------------------------------------------
    def ipv4(self) -> str:
        return ".".join(str(self.random_int(0, 255)) for _ in range(4))

    def ipv4_private(self) -> str:
        """An address from 10/8, 172.16/12 or 192.168/16."""
        block = self.random_element(("10", "172", "192"))
        if block == "10":
            octets = [10, self.random_int(0, 255), self.random_int(0, 255), self.random_int(1, 254)]
        elif block == "172":
            octets = [172, self.random_int(16, 31), self.random_int(0, 255), self.random_int(1, 254)]
        else:
            octets = [192, 168, self.random_int(0, 255), self.random_int(1, 254)]
        return ".".join(str(o) for o in octets)

    def ipv6(self) -> str:
        return ":".join(f"{self.random_int(0, 65535):x}" for _ in range(8))

    def mac_address(self) -> str:
        return ":".join(f"{self.random_int(0, 255):02x}" for _ in range(6))

    def port_number(self, is_system: bool = False, is_user: bool = False) -> int:
        if is_system:
            return self.random_int(0, 1023)
        if is_user:
            return self.random_int(1024, 49151)
        return self.random_int(0, 65535)

    # --- ASCII-guaranteed variants --------------------------------------
    # These exist for callers that need to be certain a value is ASCII.
    # Every address this provider makes already is, so they are aliases.
    def ascii_email(self) -> str:
        return self.email()

    def ascii_safe_email(self) -> str:
        return self.safe_email()

    def ascii_free_email(self) -> str:
        return self.free_email()

    def ascii_company_email(self) -> str:
        return self.company_email()

    def safe_domain_name(self) -> str:
        """A domain reserved for documentation, so it can never resolve."""
        return f"example.{self.random_element(self.safe_email_tlds)}"

    # --- HTTP -----------------------------------------------------------
    http_methods: Sequence[str] = ("GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS")
    http_statuses: Sequence[int] = (
        200, 201, 202, 204, 301, 302, 304, 400, 401, 403, 404, 405, 409, 410,
        422, 429, 500, 502, 503, 504,
    )

    def http_method(self) -> str:
        return self.random_element(self.http_methods)

    def http_status_code(self) -> int:
        return self.random_element(self.http_statuses)

    # --- address blocks -------------------------------------------------
    def ipv4_public(self) -> str:
        """An address outside the private, loopback and link-local ranges."""
        while True:
            candidate = self.ipv4()
            first, second = (int(part) for part in candidate.split(".")[:2])
            if first in (0, 10, 127) or first >= 224:
                continue
            if first == 172 and 16 <= second <= 31:
                continue
            if first == 192 and second == 168:
                continue
            if first == 169 and second == 254:
                continue
            return candidate

    def ipv4_network_class(self) -> str:
        return self.random_element(("a", "b", "c"))

    # --- registry identifiers -------------------------------------------
    def iana_id(self) -> str:
        """An IANA registrar ID."""
        return str(self.random_int(1, 8_999_999))

    def ripe_id(self) -> str:
        """A RIPE NCC organisation handle, e.g. ``ORG-AB123-RIPE``."""
        letters = self.lexify("??", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return f"ORG-{letters}{self.random_int(1, 9999)}-RIPE"

    def nic_handle(self, suffix: str = "AF") -> str:
        """A network information centre handle."""
        if suffix and suffix[0].isdigit():
            raise ValueError("suffix cannot start with a digit")
        letters = self.lexify("???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return f"{letters}{self.random_int(1, 9999)}-{suffix}" if suffix else f"{letters}{self.random_int(1, 9999)}"

    def nic_handles(self, count: int = 1, suffix: str = "AF") -> List[str]:
        return [self.nic_handle(suffix) for _ in range(count)]

    def dga(self, year: Optional[int] = None, month: Optional[int] = None, day: Optional[int] = None,
            tld: Optional[str] = None, length: int = 12) -> str:
        """A domain-generation-algorithm style name, seeded by a date.

        Used to produce look-alike malicious domains for detection testing.
        """
        from datetime import date as _date

        today = _date.today()
        seed_value = (year or today.year) * 10000 + (month or today.month) * 100 + (day or today.day)
        rng = _std_random.Random(seed_value ^ self.random_int(0, 2**31))
        name = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(length))
        return f"{name}.{tld or self.tld()}"

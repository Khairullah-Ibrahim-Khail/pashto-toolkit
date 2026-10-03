"""Base internet provider: usernames, domains, emails, addresses."""

import re
from typing import Sequence

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

    # --- slugs and domains ------------------------------------------------
    def slugify(self, value: str) -> str:
        """Lowercase ASCII slug; non-Latin text is dropped, so callers should
        pass transliterated input."""
        return _NON_ASCII.sub("-", value.lower()).strip("-")

    def tld(self) -> str:
        return self.random_element(self.tlds)

    def domain_word(self) -> str:
        word = self.slugify(self.generator.format("last_name"))
        return word or self.lexify("?????", letters="abcdefghijklmnopqrstuvwxyz")

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
        return "-".join(self.slugify(w) or "x" for w in self.generator.format("words", nb=value_count))

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

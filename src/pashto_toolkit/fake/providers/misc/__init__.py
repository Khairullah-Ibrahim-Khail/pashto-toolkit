"""Hashes, identifiers, booleans and passwords. Not language-specific."""

import hashlib
import string
import uuid as _uuid
from typing import Optional, Union

from ...core import BaseProvider


class Provider(BaseProvider):
    """Values that are the same in any language."""

    language_locale_codes = ("ps_AF", "fa_AF", "en_US", "ur_PK", "ar_SA", "tr_TR", "ru_RU")

    def boolean(self, chance_of_getting_true: int = 50) -> bool:
        return self.random_int(1, 100) <= chance_of_getting_true

    def null_boolean(self) -> Optional[bool]:
        return self.random_element((None, True, False))

    def uuid4(self, cast_to: type = str) -> Union[str, _uuid.UUID, bytes]:
        """A version-4 UUID drawn from the seeded generator, so it is reproducible."""
        value = _uuid.UUID(int=self.generator.random.getrandbits(128), version=4)
        if cast_to is str:
            return str(value)
        if cast_to is bytes:
            return value.bytes
        return value

    def binary(self, length: int = 64) -> bytes:
        return bytes(self.random_int(0, 255) for _ in range(length))

    def md5(self, raw_output: bool = False) -> Union[str, bytes]:
        digest = hashlib.md5(self.binary(16))
        return digest.digest() if raw_output else digest.hexdigest()

    def sha1(self, raw_output: bool = False) -> Union[str, bytes]:
        digest = hashlib.sha1(self.binary(16))
        return digest.digest() if raw_output else digest.hexdigest()

    def sha256(self, raw_output: bool = False) -> Union[str, bytes]:
        digest = hashlib.sha256(self.binary(16))
        return digest.digest() if raw_output else digest.hexdigest()

    def password(
        self,
        length: int = 10,
        special_chars: bool = True,
        digits: bool = True,
        upper_case: bool = True,
        lower_case: bool = True,
    ) -> str:
        """A password that contains at least one of every class requested."""
        groups = []
        if lower_case:
            groups.append(string.ascii_lowercase)
        if upper_case:
            groups.append(string.ascii_uppercase)
        if digits:
            groups.append(string.digits)
        if special_chars:
            groups.append("!@#$%^&*()-_=+")
        if not groups:
            raise ValueError("password() needs at least one character class enabled")
        if length < len(groups):
            raise ValueError(f"length must be at least {len(groups)} for the requested classes")

        chars = [self.random_element(group) for group in groups]
        pool = "".join(groups)
        chars += [self.random_element(pool) for _ in range(length - len(chars))]
        self.generator.random.shuffle(chars)
        return "".join(chars)

    def locale(self) -> str:
        return self.random_element(self.language_locale_codes)

    def hexify(self, text: str = "^^^^", upper: bool = False) -> str:
        """Replace every ``^`` with a hex digit."""
        digits = "0123456789ABCDEF" if upper else "0123456789abcdef"
        return "".join(self.random_element(digits) if c == "^" else c for c in text)

    emojis = (
        "\U0001F600", "\U0001F602", "\U0001F609", "\U0001F60D", "\U0001F914",
        "\U0001F44D", "\U0001F44F", "\U0001F64F", "\U0001F525", "\U00002B50",
        "\U00002764", "\U0001F389", "\U0001F680", "\U0001F4DA", "\U0001F4DD",
        "\U0001F30D", "\U0001F31E", "\U0001F327", "\U0001F334", "\U0001F33E",
        "\U0001F34E", "\U0001F35E", "\U0001F375", "\U0001F3E0", "\U0001F3DE",
    )

    def emoji(self) -> str:
        return self.random_element(self.emojis)

    def enum(self, enum_cls: type) -> object:
        """One member of an ``enum.Enum`` subclass."""
        import enum as _enum

        if not (isinstance(enum_cls, type) and issubclass(enum_cls, _enum.Enum)):
            raise ValueError("enum() needs an enum.Enum subclass")
        members = list(enum_cls)
        if not members:
            raise ValueError(f"{enum_cls.__name__} has no members")
        return self.random_element(members)

    def image_url(self, width: Optional[int] = None, height: Optional[int] = None,
                  placeholder_url: Optional[str] = None) -> str:
        """A placeholder image URL. Nothing is downloaded."""
        w = width or self.random_element((160, 320, 640, 800, 1024, 1280))
        h = height or self.random_element((120, 240, 480, 600, 768, 960))
        template = placeholder_url or "https://placehold.co/{width}x{height}.png"
        return template.format(width=w, height=h)

    def image(self, size: tuple = (256, 256), image_format: str = "png") -> bytes:
        """A tiny valid image file as bytes, for upload and MIME tests.

        Returns a 1x1 pixel; ``size`` is recorded in the PNG header only for
        the png format, and is otherwise advisory.
        """
        import struct
        import zlib

        if image_format != "png":
            raise ValueError("Only 'png' is supported; it needs no third-party library.")
        width, height = 1, 1
        raw = b"\x00" + bytes((self.random_int(0, 255), self.random_int(0, 255), self.random_int(0, 255)))

        def chunk(tag: bytes, payload: bytes) -> bytes:
            return (struct.pack(">I", len(payload)) + tag + payload
                    + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))

        header = struct.pack(">2I5B", width, height, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))

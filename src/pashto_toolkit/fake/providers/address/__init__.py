"""Base address provider."""

from typing import Sequence

from ...core import BaseProvider

#: Afghanistan, which is the only country these locales describe.
COUNTRY_NAME = {"pa_AF": "افغانستان", "en_AF": "Afghanistan"}
COUNTRY_CODE = "AF"


class Provider(BaseProvider):
    """Street, settlement and postcode formatting.

    The locale providers supply the Afghan data and the ``*_formats``
    templates; the methods here expand them.
    """

    city_suffixes: Sequence[str] = ()
    street_suffixes: Sequence[str] = ()
    city_formats: Sequence[str] = ("{{city}}",)
    street_name_formats: Sequence[str] = ("{{street}}",)
    street_address_formats: Sequence[str] = ("{{street}} {{building_number}}",)
    address_formats: Sequence[str] = ("{{street_address}}, {{city}}, {{postcode}}",)
    building_number_formats: Sequence[str] = ("#", "##", "###")
    postcode_formats: Sequence[str] = ("#####",)

    def city_suffix(self) -> str:
        return self.random_element(self.city_suffixes) if self.city_suffixes else ""

    def street_suffix(self) -> str:
        return self.random_element(self.street_suffixes) if self.street_suffixes else ""

    def building_number(self) -> str:
        return self.numerify(self.random_element(self.building_number_formats))

    def city(self) -> str:
        return self.parse(self.random_element(self.city_formats))

    def street_name(self) -> str:
        return self.parse(self.random_element(self.street_name_formats))

    def street_address(self) -> str:
        return self.parse(self.random_element(self.street_address_formats))

    def postcode(self) -> str:
        return self.numerify(self.random_element(self.postcode_formats))

    def address(self) -> str:
        return self.parse(self.random_element(self.address_formats))

    def current_country_code(self) -> str:
        return COUNTRY_CODE

    def current_country(self) -> str:
        return COUNTRY_NAME.get(self.generator.locale, "Afghanistan")

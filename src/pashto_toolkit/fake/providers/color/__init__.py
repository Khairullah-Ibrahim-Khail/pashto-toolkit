"""Base colour provider."""

from collections import OrderedDict
from typing import Dict, Sequence, Tuple

from ...core import BaseProvider


class Provider(BaseProvider):
    """Named colours from the locale, plus hex and RGB forms."""

    all_colors: Dict[str, str] = OrderedDict()
    safe_colors: Sequence[str] = ()

    def color_name(self) -> str:
        return self.random_element(list(self.all_colors.keys()))

    def safe_color_name(self) -> str:
        return self.random_element(self.safe_colors) if self.safe_colors else self.color_name()

    def hex_color(self) -> str:
        return f"#{self.random_int(0, 0xFFFFFF):06x}"

    def safe_hex_color(self) -> str:
        """A hex colour whose channels are each a repeated nibble."""
        return "#" + "".join(f"{self.random_int(0, 15):x}" * 2 for _ in range(3))

    def rgb_color(self) -> str:
        return ",".join(str(self.random_int(0, 255)) for _ in range(3))

    def rgb_css_color(self) -> str:
        return f"rgb({self.rgb_color()})"

    def color_rgb(self) -> Tuple[int, int, int]:
        return (self.random_int(0, 255), self.random_int(0, 255), self.random_int(0, 255))

    def color(self) -> str:
        """A hex colour. Use :meth:`color_name` for the localized name."""
        return self.hex_color()

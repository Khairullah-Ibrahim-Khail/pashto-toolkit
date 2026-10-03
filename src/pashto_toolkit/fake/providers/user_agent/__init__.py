"""Browser user-agent strings."""

from typing import Sequence

from ...core import BaseProvider


class Provider(BaseProvider):
    """Plausible user-agent strings for the major browsers."""

    windows_tokens: Sequence[str] = (
        "Windows NT 10.0; Win64; x64",
        "Windows NT 11.0; Win64; x64",
        "Windows NT 10.0; WOW64",
    )
    mac_tokens: Sequence[str] = (
        "Macintosh; Intel Mac OS X 10_15_7",
        "Macintosh; Intel Mac OS X 13_6",
        "Macintosh; Apple M2 Mac OS X 14_4",
    )
    linux_tokens: Sequence[str] = (
        "X11; Linux x86_64",
        "X11; Ubuntu; Linux x86_64",
        "X11; Fedora; Linux x86_64",
    )
    android_tokens: Sequence[str] = (
        "Linux; Android 13; Pixel 7",
        "Linux; Android 14; SM-S918B",
        "Linux; Android 12; moto g82",
    )
    ios_tokens: Sequence[str] = (
        "iPhone; CPU iPhone OS 17_4 like Mac OS X",
        "iPad; CPU OS 16_6 like Mac OS X",
    )

    def windows_platform_token(self) -> str:
        return self.random_element(self.windows_tokens)

    def mac_platform_token(self) -> str:
        return self.random_element(self.mac_tokens)

    def linux_platform_token(self) -> str:
        return self.random_element(self.linux_tokens)

    def android_platform_token(self) -> str:
        return self.random_element(self.android_tokens)

    def ios_platform_token(self) -> str:
        return self.random_element(self.ios_tokens)

    def _desktop_token(self) -> str:
        return self.random_element(
            (self.windows_platform_token(), self.mac_platform_token(), self.linux_platform_token())
        )

    def chrome(self) -> str:
        version = f"{self.random_int(110, 128)}.0.{self.random_int(1000, 6999)}.{self.random_int(10, 199)}"
        return (
            f"Mozilla/5.0 ({self._desktop_token()}) AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{version} Safari/537.36"
        )

    def firefox(self) -> str:
        version = f"{self.random_int(110, 128)}.0"
        token = self._desktop_token()
        return f"Mozilla/5.0 ({token}; rv:{version}) Gecko/20100101 Firefox/{version}"

    def safari(self) -> str:
        version = f"{self.random_int(14, 17)}.{self.random_int(0, 6)}"
        token = self.random_element((self.mac_platform_token(), self.ios_platform_token()))
        return (
            f"Mozilla/5.0 ({token}) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            f"Version/{version} Safari/605.1.15"
        )

    def opera(self) -> str:
        chrome = f"{self.random_int(110, 128)}.0.0.0"
        opr = f"{self.random_int(95, 110)}.0.0.0"
        return (
            f"Mozilla/5.0 ({self._desktop_token()}) AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{chrome} Safari/537.36 OPR/{opr}"
        )

    def edge(self) -> str:
        version = f"{self.random_int(110, 128)}.0.0.0"
        return (
            f"Mozilla/5.0 ({self.windows_platform_token()}) AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{version} Safari/537.36 Edg/{version}"
        )

    def user_agent(self) -> str:
        builder = self.random_element((self.chrome, self.firefox, self.safari, self.opera, self.edge))
        return builder()

    def internet_explorer(self) -> str:
        """A legacy Internet Explorer string, for testing old-browser paths."""
        return (
            f"Mozilla/5.0 (compatible; MSIE {self.random_int(9, 11)}.0; "
            f"{self.windows_platform_token()}; Trident/{self.random_int(5, 7)}.0)"
        )

    def linux_processor(self) -> str:
        return self.random_element(("i686", "x86_64", "aarch64", "armv7l"))

    def mac_processor(self) -> str:
        return self.random_element(("Intel", "Apple M1", "Apple M2", "Apple M3", "PPC"))

"""File names, paths, extensions and MIME types."""

from typing import Dict, Sequence

from ...core import BaseProvider


class Provider(BaseProvider):
    """Filesystem-shaped values."""

    #: MIME type -> the extensions normally used for it.
    mime_types: Dict[str, Sequence[str]] = {
        "application/json": ("json",),
        "application/msword": ("doc", "docx"),
        "application/pdf": ("pdf",),
        "application/vnd.ms-excel": ("xls", "xlsx"),
        "application/x-tar": ("tar", "gz"),
        "application/zip": ("zip",),
        "audio/mpeg": ("mp3",),
        "audio/ogg": ("ogg",),
        "image/jpeg": ("jpg", "jpeg"),
        "image/png": ("png",),
        "image/svg+xml": ("svg",),
        "image/webp": ("webp",),
        "text/csv": ("csv",),
        "text/html": ("html", "htm"),
        "text/plain": ("txt",),
        "video/mp4": ("mp4",),
        "video/x-msvideo": ("avi",),
    }

    unix_devices: Sequence[str] = ("sda", "sdb", "sdc", "nvme0n1", "nvme1n1", "vda", "mmcblk0")

    def mime_type(self, category: str = "") -> str:
        """A MIME type, optionally limited to a top-level category."""
        candidates = [t for t in self.mime_types if not category or t.startswith(f"{category}/")]
        if not candidates:
            raise ValueError(f"No MIME types in category {category!r}.")
        return self.random_element(sorted(candidates))

    def file_extension(self, category: str = "") -> str:
        return self.random_element(self.mime_types[self.mime_type(category)])

    def file_name(self, category: str = "", extension: str = "") -> str:
        """A slugged word plus an extension, so the name is path-safe."""
        stem = self.generator.format("slug", value_count=self.random_int(1, 3))
        return f"{stem}.{extension or self.file_extension(category)}"

    def file_path(
        self,
        depth: int = 1,
        category: str = "",
        extension: str = "",
        absolute: bool = True,
    ) -> str:
        parts = [self.generator.format("slug", value_count=1) for _ in range(max(0, depth))]
        path = "/".join(parts + [self.file_name(category, extension)])
        return f"/{path}" if absolute else path

    def unix_device(self, prefix: str = "") -> str:
        return f"/dev/{prefix or self.random_element(self.unix_devices)}"

    def unix_partition(self, prefix: str = "") -> str:
        return f"{self.unix_device(prefix)}{self.random_int(1, 9)}"

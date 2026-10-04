"""Serialised output: JSON, delimited text, XML and archives."""

import csv as _csv
import io
import json as _json
import tarfile
import zipfile
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from ...core import BaseProvider

#: Archive entries carry this timestamp instead of the current time, so the
#: bytes a seed produces are reproducible. 1980-01-01 is the earliest a ZIP
#: entry can record.
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

#: Default record shape: (column name, formatter name).
DEFAULT_COLUMNS: Tuple[Tuple[str, str], ...] = (
    ("name", "name"),
    ("province", "province"),
    ("phone", "phone_number"),
    ("id", "afghan_id"),
)


class _Encoder(_json.JSONEncoder):
    """Serialises the date and Decimal values the providers return."""

    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, (set, frozenset)):
            return sorted(o, key=str)
        return super().default(o)


class Provider(BaseProvider):
    """Turns generated records into the formats data pipelines expect."""

    def _rows(
        self,
        num_rows: int,
        data_columns: Optional[Sequence[Tuple[str, str]]],
    ) -> List[Dict[str, Any]]:
        columns = tuple(data_columns) if data_columns else DEFAULT_COLUMNS
        return [
            {name: self.generator.format(formatter) for name, formatter in columns}
            for _ in range(num_rows)
        ]

    # --- JSON -------------------------------------------------------------
    def json(
        self,
        data_columns: Optional[Sequence[Tuple[str, str]]] = None,
        num_rows: int = 10,
        indent: Optional[int] = None,
    ) -> str:
        """A JSON array of records."""
        return _json.dumps(self._rows(num_rows, data_columns), cls=_Encoder, indent=indent, ensure_ascii=False)

    def json_bytes(
        self,
        data_columns: Optional[Sequence[Tuple[str, str]]] = None,
        num_rows: int = 10,
        indent: Optional[int] = None,
    ) -> bytes:
        return self.json(data_columns, num_rows, indent).encode("utf-8")

    # --- delimited text ---------------------------------------------------
    def dsv(
        self,
        dialect: str = "excel",
        data_columns: Optional[Sequence[Tuple[str, str]]] = None,
        num_rows: int = 10,
        include_row_ids: bool = False,
        delimiter: str = ",",
        **kwargs: Any,
    ) -> str:
        """Delimiter-separated values, with a header row."""
        rows = self._rows(num_rows, data_columns)
        buffer = io.StringIO()
        fieldnames = (["id"] if include_row_ids else []) + list(rows[0].keys() if rows else [])
        writer = _csv.DictWriter(
            buffer, fieldnames=fieldnames, dialect=dialect, delimiter=delimiter, lineterminator="\r\n", **kwargs
        )
        writer.writeheader()
        for index, row in enumerate(rows, start=1):
            writer.writerow({**({"id": index} if include_row_ids else {}), **row})
        return buffer.getvalue()

    def csv(self, **kwargs: Any) -> str:
        return self.dsv(delimiter=",", **kwargs)

    def tsv(self, **kwargs: Any) -> str:
        return self.dsv(delimiter="\t", **kwargs)

    def psv(self, **kwargs: Any) -> str:
        return self.dsv(delimiter="|", **kwargs)

    def fixed_width(
        self,
        data_columns: Optional[Sequence[Tuple[str, str]]] = None,
        num_rows: int = 10,
        align: str = "left",
        width: int = 22,
    ) -> str:
        """Column-aligned text, one record per line."""
        if align not in ("left", "right", "center"):
            raise ValueError("align must be 'left', 'right' or 'center'")
        justify = {"left": str.ljust, "right": str.rjust, "center": str.center}[align]
        lines = []
        for row in self._rows(num_rows, data_columns):
            lines.append("".join(justify(str(value)[:width], width) for value in row.values()).rstrip())
        return "\n".join(lines)

    # --- XML --------------------------------------------------------------
    def xml(
        self,
        data_columns: Optional[Sequence[Tuple[str, str]]] = None,
        num_rows: int = 10,
        root: str = "records",
        record: str = "record",
    ) -> str:
        """A flat XML document, one element per field."""
        from xml.sax.saxutils import escape

        parts = [f"<{root}>"]
        for row in self._rows(num_rows, data_columns):
            parts.append(f"  <{record}>")
            for name, value in row.items():
                parts.append(f"    <{name}>{escape(str(value))}</{name}>")
            parts.append(f"  </{record}>")
        parts.append(f"</{root}>")
        return "\n".join(parts)

    # --- archives ---------------------------------------------------------
    def zip(
        self,
        uncompressed_size: int = 65536,
        num_files: int = 1,
        min_file_size: int = 4096,
        compression: Optional[str] = None,
    ) -> bytes:
        """A real ZIP archive, returned as bytes."""
        sizes = self._file_sizes(uncompressed_size, num_files, min_file_size)
        modes = {None: zipfile.ZIP_STORED, "bzip2": zipfile.ZIP_BZIP2, "lzma": zipfile.ZIP_LZMA,
                 "deflate": zipfile.ZIP_DEFLATED, "gzip": zipfile.ZIP_DEFLATED}
        if compression not in modes:
            raise ValueError(f"Unknown compression {compression!r}. Expected one of {sorted(k for k in modes if k)}.")
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=modes[compression]) as archive:
            for name, size in zip(self._unique_names(len(sizes)), sizes):
                # writestr(name, ...) would stamp each entry with the current
                # local time, so two calls either side of a second boundary
                # produced different bytes under the same seed.
                info = zipfile.ZipInfo(name, date_time=FIXED_TIMESTAMP)
                info.compress_type = modes[compression]
                archive.writestr(info, self.generator.format("binary", length=size))
        return buffer.getvalue()

    def tar(
        self,
        uncompressed_size: int = 65536,
        num_files: int = 1,
        min_file_size: int = 4096,
        compression: Optional[str] = None,
    ) -> bytes:
        """A real TAR archive, returned as bytes."""
        modes = {None: "w", "gzip": "w:gz", "bzip2": "w:bz2", "lzma": "w:xz"}
        if compression not in modes:
            raise ValueError(f"Unknown compression {compression!r}. Expected one of {sorted(k for k in modes if k)}.")
        sizes = self._file_sizes(uncompressed_size, num_files, min_file_size)
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode=modes[compression]) as archive:
            for name, size in zip(self._unique_names(len(sizes)), sizes):
                payload = self.generator.format("binary", length=size)
                info = tarfile.TarInfo(name=name)
                info.size = len(payload)
                info.mtime = 0          # keep the bytes reproducible
                archive.addfile(info, io.BytesIO(payload))
        return buffer.getvalue()

    def _unique_names(self, count: int) -> List[str]:
        """Distinct file names, so an archive has no duplicate entries."""
        names: List[str] = []
        while len(names) < count:
            candidate = self.generator.format("file_name", extension="bin")
            if candidate not in names:
                names.append(candidate)
            elif len(set(names)) == len(names):
                names.append(f"{len(names)}-{candidate}")
        return names

    def _file_sizes(self, total: int, num_files: int, min_file_size: int) -> List[int]:
        """Split ``total`` bytes across ``num_files``, each at least the minimum."""
        if num_files < 1:
            raise ValueError("num_files must be at least 1")
        if min_file_size * num_files > total:
            raise ValueError(
                f"{num_files} files of at least {min_file_size} bytes cannot fit in {total} bytes"
            )
        remaining = total - min_file_size * num_files
        sizes = [min_file_size] * num_files
        for index in range(num_files - 1):
            take = self.random_int(0, remaining)
            sizes[index] += take
            remaining -= take
        sizes[-1] += remaining
        return sizes

    # --- time series ------------------------------------------------------
    def time_series(
        self,
        start_date: Union[str, date] = "-30d",
        end_date: Union[str, date] = "now",
        precision: Optional[float] = None,
        num_points: int = 30,
    ) -> List[Tuple[datetime, float]]:
        """``num_points`` evenly spaced ``(timestamp, value)`` pairs."""
        from datetime import timedelta

        end = datetime.now() if end_date == "now" else (
            datetime.combine(end_date, datetime.min.time()) if isinstance(end_date, date) else datetime.now()
        )
        start = end - timedelta(days=30) if isinstance(start_date, str) else datetime.combine(
            start_date, datetime.min.time()
        )
        if num_points < 2:
            raise ValueError("num_points must be at least 2")
        step = (end - start) / (num_points - 1)
        scale = precision if precision is not None else 1.0
        return [
            (start + step * index, round(self.generator.random.gauss(0, 1) * scale, 6))
            for index in range(num_points)
        ]

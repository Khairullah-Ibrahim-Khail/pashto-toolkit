"""The package must stand alone: no third-party imports anywhere in it."""

import ast
import pathlib

import pashto_toolkit

PACKAGE_ROOT = pathlib.Path(pashto_toolkit.__file__).parent

#: Only the standard library is allowed.
ALLOWED_TOP_LEVEL = {
    "ast", "collections", "datetime", "decimal", "importlib", "pathlib", "random",
    "re", "string", "sys", "types", "typing", "unicodedata", "pashto_toolkit",
}


def _modules():
    return sorted(PACKAGE_ROOT.rglob("*.py"))


def test_the_package_has_modules_to_check():
    assert len(_modules()) > 40


def test_no_module_imports_a_third_party_package():
    offenders = []
    for path in _modules():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                # level > 0 is a relative import, always within this package.
                names = [] if node.level else [(node.module or "").split(".")[0]]
            else:
                continue
            for name in names:
                if name and name not in ALLOWED_TOP_LEVEL:
                    rel = path.relative_to(PACKAGE_ROOT)
                    offenders.append(f"{rel}:{node.lineno}: imports {name!r}")
    assert not offenders, "third-party imports found:\n" + "\n".join(offenders)


def test_faker_is_not_referenced_at_all():
    offenders = []
    for path in _modules():
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if "faker" in line.lower() and "pashtofaker" not in line.lower().replace(" ", ""):
                offenders.append(f"{path.relative_to(PACKAGE_ROOT)}:{lineno}: {line.strip()}")
    assert not offenders, "references to faker remain:\n" + "\n".join(offenders)

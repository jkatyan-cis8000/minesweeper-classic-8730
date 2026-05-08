#!/usr/bin/env python3
"""
Lint.py - Enforces source architecture rules for Minesweeper.

Rules:
1. Every file under src/ belongs in exactly one layer directory.
2. Imports may only target layers in the file's own "may import from" set.
3. No file exceeds 300 lines.
4. Parses Python files using ast module.
"""

import ast
import os
import sys
from pathlib import Path

# Layer definitions and allowed import dependencies
LAYER_DEPS = {
    "types": {"types"},
    "config": {"types", "config"},
    "utils": {"utils"},
    "service": {"types", "config", "utils", "service"},
    "ui": {"types", "config", "utils", "service", "ui"},
}

VALID_LAYERS = set(LAYER_DEPS.keys())
SRC_DIR = Path("src")
MAX_LINES = 300


def get_layer_from_path(filepath: Path) -> str | None:
    """Determine which layer a file belongs to based on its directory."""
    try:
        rel_path = filepath.relative_to(SRC_DIR)
        parts = rel_path.parts
        if len(parts) > 0:
            layer = parts[0]
            if layer in VALID_LAYERS:
                return layer
    except ValueError:
        pass
    return None


def get_imports(filepath: Path) -> list[str]:
    """Extract all import module names from a Python file."""
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=str(filepath))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split(".")[0])
    except SyntaxError:
        pass
    return imports


def check_file_lines(filepath: Path) -> list[str]:
    """Check if file exceeds MAX_LINES. Returns list of violations."""
    violations = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > MAX_LINES:
            violations.append(f"{filepath}:{len(lines)}: File exceeds {MAX_LINES} lines ({len(lines)} lines)")
    except Exception:
        pass
    return violations


def check_imports(filepath: Path) -> list[str]:
    """Check that imports respect layer dependencies."""
    violations = []
    layer = get_layer_from_path(filepath)
    if layer is None:
        return violations

    allowed = LAYER_DEPS[layer]
    imports = get_imports(filepath)

    for imp in imports:
        # Check if import is a layer module (e.g., "from types import X" or "import types")
        if imp in VALID_LAYERS and imp not in allowed:
            violations.append(f"{filepath}: Import '{imp}' not allowed from layer '{layer}'")

    return violations


def check_file_location(filepath: Path) -> list[str]:
    """Check that file is inside a valid layer directory."""
    violations = []

    # Get absolute path and make relative to SRC_DIR
    abs_path = filepath.resolve()
    try:
        rel_path = abs_path.relative_to(SRC_DIR.resolve())
        parts = rel_path.parts

        # Skip if not under src/
        if len(parts) == 0 or parts[0] != "src":
            return violations

        layer = get_layer_from_path(filepath)
        if layer is None:
            violations.append(f"{filepath}: File not in a valid layer directory (expected one of: {', '.join(sorted(VALID_LAYERS))})")
    except ValueError:
        # Not under SRC_DIR
        return violations
    except Exception:
        pass

    return violations


def lint() -> list[str]:
    """Run all lint checks on Python files under src/."""
    violations = []

    for root, _, files in os.walk(SRC_DIR):
        for filename in files:
            if not filename.endswith(".py"):
                continue

            filepath = Path(root) / filename
            violations.extend(check_file_location(filepath))
            violations.extend(check_file_lines(filepath))
            violations.extend(check_imports(filepath))

    return violations


def main():
    """Main entry point."""
    violations = lint()

    if violations:
        print("Lint failed with the following violations:\n", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        sys.exit(1)

    print("Lint passed!")
    sys.exit(0)


if __name__ == "__main__":
    main()

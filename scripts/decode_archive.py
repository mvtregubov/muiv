#!/usr/bin/env python3
"""Convert the bundled Base64 archive into a ZIP file.

This script exists for situations when GitHub refuses to show binary files
("Binary file not shown") or when downloading `project_archive.zip` directly
is not possible.  It simply decodes `project_archive.base64` into a ZIP file
in the same directory.
"""
from __future__ import annotations

import argparse
import base64
from pathlib import Path


def decode_archive(source: Path, destination: Path, overwrite: bool = False) -> Path:
    """Decode `source` Base64 file into `destination` ZIP archive."""
    if destination.exists() and not overwrite:
        raise FileExistsError(
            f"Destination file '{destination}' already exists. Use --force to overwrite."
        )

    data = source.read_text()
    destination.write_bytes(base64.b64decode(data))
    return destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild project_archive.zip from project_archive.base64"
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("project_archive.base64"),
        help="Path to the Base64-encoded archive (default: project_archive.base64)",
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path("project_archive.zip"),
        help="Path where the decoded ZIP will be written (default: project_archive.zip)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite destination file if it already exists.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    archive_path = decode_archive(args.source, args.destination, overwrite=args.force)
    print(f"Decoded archive saved to {archive_path}")


if __name__ == "__main__":
    main()

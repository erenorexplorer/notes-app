"""
Create a readable snapshot of the project for pasting into ChatGPT.

Default behavior:
- Reads files from the ./app folder
- Writes one Markdown file: ./project_snapshot.md
- Includes a file map first
- Then includes the contents of each included file

Run from the project root:

    python tools/snapshot_project.py

Optional:

    python tools/snapshot_project.py --source app --output current_snapshot.md
"""

from pathlib import Path
import argparse
from datetime import datetime


# Files/folders we do not want to include in the snapshot.
SKIP_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "env",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    "_tools",
    "_docs",
}

SKIP_FILES = {
    ".env",
    "project_snapshot.md",
    "current_snapshot.md",
}

# Keep this narrow at first.
INCLUDED_EXTENSIONS = {
    ".py",
}

# Prevent accidentally dumping a huge file into the snapshot.
MAX_FILE_SIZE_BYTES = 100_000


def should_skip_path(path: Path) -> bool:
    """Return True if this path should be ignored."""
    if any(part in SKIP_DIRS for part in path.parts):
        return True

    if path.name in SKIP_FILES:
        return True

    return False


def should_include_file(path: Path) -> bool:
    """Return True if this file should be included in the snapshot."""
    if should_skip_path(path):
        return False

    if path.suffix not in INCLUDED_EXTENSIONS:
        return False

    if path.stat().st_size > MAX_FILE_SIZE_BYTES:
        return False

    return True


def get_project_files(source_dir: Path) -> list[Path]:
    """Find all included files under source_dir."""
    files = []

    for path in source_dir.rglob("*"):
        if path.is_file() and should_include_file(path):
            files.append(path)

    return sorted(files)


def build_file_map(source_dir: Path, files: list[Path]) -> str:
    """Create a simple tree-style file map."""
    lines = [f"{source_dir.name}/"]
    seen_dirs = set()

    for file_path in files:
        relative_path = file_path.relative_to(source_dir)
        parts = relative_path.parts

        # Add parent directories first
        for depth in range(len(parts) - 1):
            dir_path = parts[: depth + 1]

            if dir_path not in seen_dirs:
                indent = "  " * (depth + 1)
                lines.append(f"{indent}{parts[depth]}/")
                seen_dirs.add(dir_path)

        # Add the file
        file_indent = "  " * len(parts)
        lines.append(f"{file_indent}{parts[-1]}")

    return "\n".join(lines)


def read_file_text(path: Path) -> str:
    """Read a text file safely."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "[Skipped: could not decode as UTF-8 text]"


def build_snapshot(source_dir: Path, files: list[Path]) -> str:
    """Build the full Markdown snapshot."""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sections = [
        "# Project Snapshot",
        "",
        f"Created: {created_at}",
        f"Source folder: `{source_dir}`",
        "",
        "## File Map",
        "",
        "```text",
        build_file_map(source_dir, files),
        "```",
        "",
        "---",
        "",
        "## File Contents",
        "",
    ]

    for file_path in files:
        relative_path = file_path.relative_to(source_dir)
        contents = read_file_text(file_path)

        sections.extend(
            [
                f"### `{source_dir.name}/{relative_path}`",
                "",
                "```python",
                contents,
                "```",
                "",
                "---",
                "",
            ]
        )

    return "\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a Markdown snapshot of project source files."
    )

    parser.add_argument(
        "--source",
        default="app",
        help="Folder to snapshot. Default: app",
    )

    parser.add_argument(
        "--output",
        default="project_snapshot.md",
        help="Output Markdown file. Default: project_snapshot.md",
    )

    args = parser.parse_args()

    source_dir = Path(args.source)
    output_file = Path(args.output)

    if not source_dir.exists():
        raise FileNotFoundError(f"Source folder does not exist: {source_dir}")

    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a folder: {source_dir}")

    files = get_project_files(source_dir)
    snapshot = build_snapshot(source_dir, files)

    output_file.write_text(snapshot, encoding="utf-8")

    print(f"Snapshot created: {output_file}")
    print(f"Files included: {len(files)}")


if __name__ == "__main__":
    main()
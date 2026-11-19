"""Markdown heading-aware runbook chunks."""
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    filename: str
    section_title: str
    content: str


def split_runbook(path: Path, root: Path) -> list[Chunk]:
    filename = path.relative_to(root).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    title = path.stem
    parent = ""
    content: list[str] = []
    result: list[Chunk] = []
    fenced = False

    def flush() -> None:
        text = "\n".join(content).strip()
        if text:
            identity = hashlib.sha256(
                f"{filename}\0{title}\0{len(result)}\0{text}".encode()
            ).hexdigest()
            result.append(Chunk(identity, filename, title, text))
        content.clear()

    for line in lines:
        if re.match(r"^\s*(```|~~~)", line):
            fenced = not fenced
        match = None if fenced else re.match(r"^(#{1,3})\s+(.+?)\s*#*\s*$", line)
        if match:
            flush()
            level, heading = len(match.group(1)), match.group(2)
            if level == 1:
                parent = ""
                title = heading
            elif level == 2:
                parent = heading
                title = heading
            else:
                title = f"{parent} > {heading}" if parent else heading
        else:
            content.append(line)
    flush()
    return result

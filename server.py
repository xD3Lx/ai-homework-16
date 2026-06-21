from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import uuid

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("mcp-server-notes")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
NOTES_FILE = DATA_DIR / "notes.json"


def ensure_file_exists():
    DATA_DIR.mkdir(exist_ok=True)

    if not NOTES_FILE.exists():
        NOTES_FILE.write_text("[]", encoding="utf-8")


def load_notes() -> list[dict[str, Any]]:
    ensure_file_exists()

    raw = NOTES_FILE.read_text(encoding="utf-8").strip()
    if not raw:
        return []

    notes = json.loads(raw)

    return notes


def save_notes(notes: list[dict[str, Any]]) -> None:
    ensure_file_exists()
    content = json.dumps(notes, ensure_ascii=False, indent=2)
    NOTES_FILE.write_text(content, encoding="utf-8")


def generate_note_id() -> str:
    return str(uuid.uuid4())


@mcp.tool()
def create_note(text: str, tag: str = "default") -> dict[str, Any]:
    text = text.strip()
    tag = tag.strip().lower() if tag.strip() else "default"

    if not text:
        return {
            "status": "error",
            "message": "Note text should not be empty.",
        }

    notes = load_notes()

    note = {
        "id": generate_note_id(),
        "text": text,
        "tag": tag,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    notes.append(note)
    save_notes(notes)

    return {
        "status": "success",
        "message": "Note created successfully.",
        "note": note,
    }


@mcp.tool()
def search_notes(query: str, tag: str | None = None) -> dict[str, Any]:
    query = query.strip().lower()
    tag = tag.strip().lower() if tag else None

    if not query:
        return {
            "status": "error",
            "message": "Search query should not be empty.",
            "results": [],
        }

    notes = load_notes()
    results = []

    for note in notes:
        note_text = str(note.get("text", "")).lower()
        note_tag = str(note.get("tag", "")).lower()

        if (query in note_text) and (tag is None or tag == note_tag):
            results.append(note)

    return {
        "status": "success",
        "query": query,
        "tag": tag,
        "count": len(results),
        "results": results,
    }



@mcp.resource("notes://summary")
def notes_summary() -> str:
    notes = load_notes()

    tags: dict[str, int] = {}

    for note in notes:
        tag = str(note.get("tag", "default"))
        tags[tag] = tags.get(tag, 0) + 1

    summary = {
        "total_notes": len(notes),
        "tags": tags,
        "notes": notes,
    }

    return json.dumps(summary, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
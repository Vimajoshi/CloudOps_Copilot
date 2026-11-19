"""Evaluate the configured retriever without calling the chat model.

Run from the repository root after installing the app and indexing the runbooks:
    python evaluation/retrieval.py
Uses the same database, embedding provider, distance threshold, and top-k settings
as the application. Remote embedding requests can incur charges.
"""

import json
import pathlib
import sys

# Make the repository's app package available when run as a script.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from app.config import get_settings  # noqa: E402
from app.services import retrieve  # noqa: E402


def main():
    settings = get_settings()
    if settings.retrieval_top_k < 3:
        print("Set RETRIEVAL_TOP_K to at least 3 before running this evaluation.", file=sys.stderr)
        return 1
    cases = json.loads(pathlib.Path(__file__).with_name("incidents.json").read_text(encoding="utf-8"))
    if not cases:
        print("The evaluation dataset is empty.", file=sys.stderr)
        return 1
    hits = 0
    errors = 0
    for index, case in enumerate(cases, 1):
        try:
            chunks = retrieve(case["incident"])[:3]
            actual = {str(chunk["filename"]).replace("\\", "/").split("/")[-1] for chunk in chunks}
            hit = case["expected_filename"] in actual
            hits += hit
            print(f"{index:02d} {'HIT ' if hit else 'MISS'} expected={case['expected_filename']} retrieved={sorted(actual)}")
        except Exception as exc:
            errors += 1
            print(f"{index:02d} ERROR expected={case['expected_filename']}: {exc}", file=sys.stderr)
    print(f"Top-3 filename hit rate: {hits}/{len(cases)} ({hits / len(cases):.1%}); request errors: {errors}")
    print(f"Chunks beyond cosine distance {settings.retrieval_max_distance} are excluded.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

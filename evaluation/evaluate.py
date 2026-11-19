"""Measure end-to-end citation hits against a running, indexed Copilot API.

Usage: python evaluation/evaluate.py --url http://localhost:8000
The API and embedding/LLM providers must be configured and runbooks ingested first.
Each request may consume provider tokens and incur charges.
"""

import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://localhost:8000", help="Copilot API base URL")
    parser.add_argument("--dataset", type=pathlib.Path, default=pathlib.Path(__file__).with_name("incidents.json"))
    parser.add_argument("--timeout", type=float, default=90)
    args = parser.parse_args()
    cases = json.loads(args.dataset.read_text(encoding="utf-8"))
    if not cases:
        parser.error("dataset must contain at least one case")
    hits = 0
    errors = 0
    for index, case in enumerate(cases, 1):
        payload = json.dumps({"incident": case["incident"]}).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        api_key = os.getenv("CLOUDOPS_EVAL_API_KEY")
        if api_key:
            headers["X-API-Key"] = api_key
        request = urllib.request.Request(
            args.url.rstrip("/") + "/diagnose", data=payload,
            headers=headers, method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=args.timeout) as response:
                result = json.load(response)
            actual = {str(item.get("filename", "")).replace("\\", "/").split("/")[-1]
                      for item in result.get("citations", [])}
            hit = case["expected_filename"] in actual
            hits += hit
            print(f"{index:02d} {'HIT ' if hit else 'MISS'} expected={case['expected_filename']} cited={sorted(actual)}")
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
            errors += 1
            print(f"{index:02d} ERROR expected={case['expected_filename']}: {exc}", file=sys.stderr)
    print(f"End-to-end citation hit rate: {hits}/{len(cases)} ({hits / len(cases):.1%}); request errors: {errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

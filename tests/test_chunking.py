from app.chunking import split_runbook


def test_sections_and_code_fences(tmp_path):
    path = tmp_path / "pod.md"
    path.write_text("# Pod\nOverview\n## Diagnosis\nInspect logs\n### Commands\n```sh\n## not a heading\n```\n", encoding="utf-8")
    chunks = split_runbook(path, tmp_path)
    assert [c.section_title for c in chunks] == ["Pod", "Diagnosis", "Diagnosis > Commands"]
    assert "## not a heading" in chunks[-1].content
    assert all(c.filename == "pod.md" for c in chunks)
    assert len({c.chunk_id for c in chunks}) == 3

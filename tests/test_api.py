from types import SimpleNamespace

from fastapi.testclient import TestClient

from app import services
from app.main import app

client = TestClient(app)


def test_uncovered_incident_does_not_call_llm(monkeypatch):
    monkeypatch.setattr(services, "retrieve", lambda _: [])
    response = client.post("/diagnose", json={"incident": "unknown failure"})
    assert response.status_code == 200
    assert response.json()["covered"] is False
    assert response.json()["remediation_steps"] == []


def test_citations_must_reference_retrieved_chunks(monkeypatch):
    chunks = [{"chunk_id": "a", "filename": "pod.md", "section_title": "Diagnosis", "content": "inspect logs"}]
    monkeypatch.setattr(services, "retrieve", lambda _: chunks)

    def generate(**kwargs):
        return SimpleNamespace(usage=None, choices=[SimpleNamespace(message=SimpleNamespace(
            content='{"covered":true,"summary":"Pod failure","remediation_steps":[{"instruction":"Inspect logs","chunk_ids":["a"]}]}'))])

    monkeypatch.setattr(services.providers, "client", lambda: SimpleNamespace(chat=SimpleNamespace(
        completions=SimpleNamespace(create=generate))))
    response = client.post("/diagnose", json={"incident": "pod failure"})
    assert response.status_code == 200
    assert response.json()["citations"][0]["filename"] == "pod.md"
    assert response.json()["remediation_steps"][0]["citations"][0]["chunk_id"] == "a"

    def invalid(**kwargs):
        return SimpleNamespace(usage=None, choices=[SimpleNamespace(message=SimpleNamespace(
            content='{"covered":true,"summary":"Failure","remediation_steps":[{"instruction":"Fix","chunk_ids":["invented"]}]}'))])

    monkeypatch.setattr(services.providers, "client", lambda: SimpleNamespace(chat=SimpleNamespace(
        completions=SimpleNamespace(create=invalid))))
    assert client.post("/diagnose", json={"incident": "pod failure"}).json()["covered"] is False


def test_liveness_and_input_validation():
    assert client.get("/livez").status_code == 200
    assert client.post("/diagnose", json={"incident": ""}).status_code == 422

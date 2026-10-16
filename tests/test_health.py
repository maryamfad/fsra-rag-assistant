from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_health_ok(monkeypatch):
    monkeypatch.setattr(main, "check_db", lambda url: True)
    monkeypatch.setattr(main, "check_redis", lambda url: True)
    body = client.get("/health").json()
    assert body == {"status": "ok", "components": {"database": True, "redis": True}}


def test_health_degraded_names_the_failure(monkeypatch):
    monkeypatch.setattr(main, "check_db", lambda url: False)
    monkeypatch.setattr(main, "check_redis", lambda url: True)
    body = client.get("/health").json()
    assert body["status"] == "degraded"
    assert body["components"]["database"] is False

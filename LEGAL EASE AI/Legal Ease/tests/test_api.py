import os

os.environ["DEMO_MODE"] = "true"
os.environ["GEMINI_API_KEY"] = ""


from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(
    app
)


def test_root():

    response = client.get(
        "/"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200


def test_generate_document():

    response = client.post(
        "/generate",
        json={
            "document_type": "NDA",
            "parties": (
                "Alice Smith "
                "(Disclosing Party), "
                "Beta Ltd "
                "(Receiving Party)"
            ),
            "terms": (
                "Keep information confidential; "
                "Return information on request"
            ),
            "effective_date": "2026-10-05",
            "brand_name": "Beta Ltd"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["success"] is True

    assert (
        "NDA"
        in data["content"]
    )

    assert (
        "confidential"
        in data["content"].lower()
    )
    
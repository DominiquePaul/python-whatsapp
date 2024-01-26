from fastapi.testclient import TestClient
import pytest
from myapp.main import app


client = TestClient(app)


def test_verification_fails():
    """
    Test webhook verification mechanism.
    """
    challenge_value = "challenge"

    response = client.get(
        "/api/webhook",
        params={
            "hub.mode": "subscribe",
            # Must match the VERIFY_TOKEN env variable.
            "hub.verify_token": "bad_token",
            "hub.challenge": challenge_value,
        },
    )
    assert response.status_code == 403
    assert response.content == b"Verification token mismatch"


@pytest.mark.asyncio
async def test_valid_whatsapp_message():
    # Arrange
    data = {
        "object": "whatsapp",
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "text": "Hello",
                                    "from": "1234567890",
                                    "timestamp": 1631234567,
                                }
                            ]
                        }
                    }
                ]
            }
        ],
    }

    # Act

    response = client.post("/api/webhook", json=data)

    # Assert
    assert response.status_code == 200
    assert response.content == b'"ok"'

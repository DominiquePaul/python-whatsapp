import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_verification_fails():
    """
    Test webhook verification mechanism.
    """
    challenge_value = "challenge"

    response = client.get(
        "/api/whatsapp",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "bad_token",
            "hub.challenge": challenge_value,
        },
    )
    assert response.status_code == 403
    assert response.content == b"Verification token mismatch"


@pytest.mark.asyncio
async def test_valid_whatsapp_message(mocker, example_text_message):
    # Arrange
    data = example_text_message.model_dump(mode="json")
    mock_send_message = mocker.AsyncMock()
    mocker.patch("whatsapp.send_message", new=mock_send_message)
    # or whatever the send_message is supposed to return
    mock_send_message.return_value = True

    response = client.post("/api/whatsapp", json=data)

    # Assert
    assert response.status_code == 200
    assert response.content == b'"ok"'

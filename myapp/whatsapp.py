import httpx
import requests
import myapp.config as cfg
import logging
from fastapi import HTTPException
from dataclasses import dataclass, field
import myapp.constants as c


@dataclass
class WamBase:
    message_id: str
    wa_id: str
    profile_name: str
    message_type: str
    timestamp: str
    message_body: str = field(default_factory=str, kw_only=True)


@dataclass
class WamMediaType(WamBase):
    mime_type: str
    media_id: str
    media_bytes: bytes = field(default_factory=bytes)


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.object
        and body.entry[0].get("changes")
        and body.entry[0]["changes"][0].get("value")
        and body.entry[0]["changes"][0]["value"].get("messages")
        and body.entry[0]["changes"][0]["value"]["messages"][0]
    )


async def parse_whatsapp_message(body: c.WebhookRequestData) -> WamBase:
    values = body.entry[0]["changes"][0]["value"]
    wa_id = values["contacts"][0]["wa_id"]
    name = values["contacts"][0]["profile"]["name"]
    message = values["messages"][0]
    timestamp = message["timestamp"]
    message_type = message["type"]
    message_id = message["id"]

    if message_type == "text":
        wam_text = WamBase(
            message_id=message_id,
            wa_id=wa_id,
            profile_name=name,
            message_type=message_type,
            timestamp=timestamp,
            message_body=message["text"]["body"],
        )
        return wam_text
    elif message_type in ["audio", "document", "image"]:
        wam_media = WamMediaType(
            message_id=message_id,
            wa_id=wa_id,
            profile_name=name,
            message_type=message_type,
            timestamp=timestamp,
            mime_type=message[message_type]["mime_type"],
            media_id=message[message_type]["id"],
        )
        wam_media.media_bytes = await _download_media(wam_media.media_id)
        return wam_media
    else:
        raise ValueError(
            f"message type: '{message_type}' not one of [text, audio, document, image]"
        )


async def _download_media(media_id) -> bytes:
    endpoint = f"https://graph.facebook.com/{cfg.WHATSAPP_API_VERSION}/{media_id}"
    headers = {"Authorization": f"Bearer {cfg.WHATSAPP_TOKEN}"}

    # get download url
    with httpx.Client(timeout=10) as client:  # 10 seconds timeout
        response = client.get(endpoint, headers=headers)
    download_url = response.json()["url"]

    # download the memo itself
    async with httpx.AsyncClient() as client:
        response = await client.get(download_url, headers=headers)
        response.raise_for_status()
        return response.content


async def _post_httpx_request(url, data=None, files=None) -> dict:
    headers = {"Authorization": f"Bearer {cfg.WHATSAPP_TOKEN}"}
    if bool(data):
        headers["Content-type"] = "application/json"
    try:
        with httpx.Client(timeout=10) as client:  # 10 seconds timeout
            response = client.post(url, json=data, headers=headers, files=files)
            response.raise_for_status()
    except (requests.Timeout, httpx.ReadTimeout):
        logging.error("Timeout occurred while sending message")
        raise HTTPException(status_code=408, detail="Request timed out")

    except (requests.RequestException, httpx.RequestError) as e:
        logging.error(f"Request failed due to: {e}")
        raise HTTPException(status_code=500, detail="Failed to send message")
    else:
        r = response.json()
        # This is only False when we upload the file. For all other cases - sending a message -
        # we want more information such as the message id.
        if bool(data):
            if len(r["contacts"]) > 1 or len(r["messages"]) > 1:
                raise ValueError(
                    "More than one contact returned after making post request, expected only one."
                )

            out = {}
            out["messaging_product"] = r["messaging_product"]
            out["contacts_input"] = r["contacts"][0]["input"]
            out["contacts_wa_id"] = r["contacts"][0]["wa_id"]
            out["messages_id"] = r["messages"][0]["id"]

        return r


async def send_message(recipient_id: str, message: str):
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "text",
        "text": {"preview_url": False, "body": message},
    }
    url = f"https://graph.facebook.com/{cfg.WHATSAPP_API_VERSION}/{cfg.PHONE_NUMBER_ID}/messages"
    return await _post_httpx_request(url, data=data)


async def send_quick_reply_message(recipient_id: str, message: str, buttons: list[str]):
    endpoint = f"https://graph.facebook.com/{cfg.WHATSAPP_API_VERSION}/{cfg.PHONE_NUMBER_ID}/messages"
    btns = []
    for idx, b in enumerate(buttons):
        btns.append({"type": "reply", "reply": {"id": f"choice{idx+1}", "title": b}})
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": message},
            "action": {"buttons": btns},
        },
    }
    return await _post_httpx_request(endpoint, data=data)


async def _upload_media(file_data: bytes, file_name: str, mime_type: str) -> dict:
    endpoint = f"https://graph.facebook.com/{cfg.WHATSAPP_API_VERSION}/{cfg.PHONE_NUMBER_ID}/media"

    # Multipart form data
    files = {
        "file": (file_name, file_data, mime_type),
        "type": (None, "application/json"),
        "messaging_product": (None, "whatsapp"),
    }

    # Send the request
    response = await _post_httpx_request(endpoint, files=files)
    return response


async def send_pdf(recipient_id: str, file_data: bytes, file_name: str, mime_type: str):
    media_id = (await _upload_media(file_data, file_name, mime_type))["id"]
    endpoint = f"https://graph.facebook.com/{cfg.WHATSAPP_API_VERSION}/{cfg.PHONE_NUMBER_ID}/messages"
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "document",
        "document": {"filename": file_name, "id": media_id},
    }
    return await _post_httpx_request(endpoint, data=data)

import httpx
import whatsapp.config as cfg
from dataclasses import dataclass, field
import whatsapp.constants as c


@dataclass
class WamBase:
    webhook_id: str
    wamid: str
    phone_number_id: str
    wa_id: str
    profile_name: str
    message_type: str
    timestamp: str
    message_body: str = field(default="", kw_only=True)
    reference_wamid: str | None = field(default=None, kw_only=True)
    reference_message_user_phone: str | None = field(default=None, kw_only=True)


@dataclass
class WamMediaType(WamBase):
    mime_type: str
    media_id: str
    media_bytes: bytes = field(default=b"")


def is_valid_whatsapp_message(body: c.WebhookRequestData) -> bool:
    """
    Validates the structure of the incoming webhook event to ensure it contains a WhatsApp message.

    Args:
        body (c.WebhookRequestData): The incoming webhook request data.

    Returns:
        bool: True if the message structure is valid, False otherwise.
    """
    try:
        return bool(body.entry[0]["changes"][0]["value"]["messages"][0])
    except (IndexError, KeyError):
        return False


async def parse_whatsapp_message(body: c.WebhookRequestData) -> WamBase:
    """
    Parse the incoming webhook request data and return an instance of WamBase or WamMediaType.

    This function extracts the necessary information from the webhook request data to
    instantiate and return a WamBase dataclass object for text messages or a WamMediaType
    dataclass object for media messages (audio, document, image). If the message type is
    unsupported, it raises a ValueError.

    Args:
        body (c.WebhookRequestData): The incoming webhook request data.

    Returns:
        WamBase: An instance of WamBase for text messages.
        WamMediaType: An instance of WamMediaType for media messages.
    """
    values = body.entry[0]["changes"][0]["value"]
    message = values["messages"][0]
    wam_data = {
        "webhook_id": body.entry[0]["id"],
        "wamid": message["id"],
        "phone_number_id": values["metadata"]["phone_number_id"],
        "wa_id": values["contacts"][0]["wa_id"],
        "profile_name": values["contacts"][0]["profile"]["name"],
        "message_type": message["type"],
        "timestamp": message["timestamp"],
    }

    if message.get("context"):
        wam_data.update(
            {
                "reference_wamid": message["context"]["id"],
                "reference_message_user_phone": message["context"]["from"],
            }
        )
    if message["type"] == "text":
        wam_data["message_body"] = message["text"]["body"]
    elif message["type"] in ["audio", "document", "image"]:
        wam_data.update(
            {
                "mime_type": message[message["type"]]["mime_type"],
                "media_id": message[message["type"]]["id"],
            }
        )
        wam_media = WamMediaType(**wam_data)
        wam_media.media_bytes = await _download_media(wam_media.media_id)
        return wam_media
    else:
        raise ValueError(f"Unsupported message type: '{message['type']}'")

    return WamBase(**wam_data)


async def _download_media(media_id) -> bytes:
    """
    Download media from the given media_id.

    This function uses the media_id to construct a URL to the media file,
    sends a GET request to that URL, and returns the content of the response.
    If the media file cannot be found or accessed, an HTTP error is raised.

    Args:
        media_id (str): The ID of the media file to download.

    Returns:
        bytes: The content of the media file.
    """
    endpoint = f"https://graph.facebook.com/{cfg.WHATSAPP_API_VERSION}/{media_id}"
    headers = {"Authorization": f"Bearer {cfg.WHATSAPP_TOKEN}"}

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(endpoint, headers=headers)
        response.raise_for_status()
        download_url = response.json()["url"]

        response = await client.get(download_url, headers=headers)
        response.raise_for_status()
        return response.content


async def _post_httpx_request(
    url: str, data: dict | None = None, files: dict | None = None
) -> dict:
    """
    Send a POST request to the given URL with the provided data and files.

    This function constructs a POST request with the given data and files,
    sends the request to the given URL, and returns the JSON content of the response.
    If the response contains more than one contact or message, a ValueError is raised.

    Args:
        url (str): The URL to send the POST request to.
        data (dict, optional): The data to include in the request body. Defaults to None.
        files (dict, optional): The files to include in the request body. Defaults to None.

    Returns:
        dict: The JSON content of the response.
    """
    headers = {"Authorization": f"Bearer {cfg.WHATSAPP_TOKEN}"}
    if data:
        headers["Content-Type"] = "application/json"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=data, headers=headers, files=files)
        response.raise_for_status()

    r = response.json()
    if data and (
        "contacts" in r
        and len(r["contacts"]) > 1
        or "messages" in r
        and len(r["messages"]) > 1
    ):
        raise ValueError("Expected only one contact and one message in the response.")

    return r


async def send_message(recipient_id: str, message: str) -> dict:
    """
    Send a text message to the recipient.

    This function constructs a message with the given recipient_id and message,
    sends the message to the recipient, and returns the JSON content of the response.

    Args:
        recipient_id (str): The ID of the recipient to send the message to.
        message (str): The message to send.

    Returns:
        dict: The JSON content of the response.
    """
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "text",
        "text": {"preview_url": False, "body": message},
    }
    url = f"https://graph.facebook.com/{cfg.WHATSAPP_API_VERSION}/{cfg.WHATSAPP_PHONE_NUMBER_ID}/messages"
    return await _post_httpx_request(url, data=data)


async def send_quick_reply_message(
    recipient_id: str, message: str, buttons: list[str]
) -> dict:
    """
    Send a quick reply message with buttons to the recipient.

    This function constructs a message with the given recipient_id and message,
    adds quick reply buttons, sends the message to the recipient, and returns
    the JSON content of the response.

    Args:
        recipient_id (str): The ID of the recipient to send the message to.
        message (str): The message to send.
        buttons (list[str]): A list of button titles for quick replies.

    Returns:
        dict: The JSON content of the response.
    """
    btns = [
        {"type": "reply", "reply": {"id": f"choice{idx+1}", "title": b}}
        for idx, b in enumerate(buttons)
    ]
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
    endpoint = f"https://graph.facebook.com/{cfg.WHATSAPP_API_VERSION}/{cfg.WHATSAPP_PHONE_NUMBER_ID}/messages"
    return await _post_httpx_request(endpoint, data=data)


async def _upload_media(file_data: bytes, file_name: str, mime_type: str) -> dict:
    """
    Uploads a media file to the server.

    Args:
        file_data (bytes): The data of the file to be uploaded.
        file_name (str): The name of the file to be uploaded.
        mime_type (str): The MIME type of the file to be uploaded.

    Returns:
        dict: The JSON content of the response.
    """
    files: dict = {
        "file": (file_name, file_data, mime_type),
        "type": (None, "application/json"),
        "messaging_product": (None, "whatsapp"),
    }
    endpoint: str = f"https://graph.facebook.com/{cfg.WHATSAPP_API_VERSION}/{cfg.WHATSAPP_PHONE_NUMBER_ID}/media"
    return await _post_httpx_request(endpoint, files=files)


async def send_pdf(
    recipient_id: str, file_data: bytes, file_name: str, mime_type: str
) -> dict:
    """
    Sends a PDF file to the specified recipient on WhatsApp.

    Args:
        recipient_id (str): The ID of the recipient to send the PDF to.
        file_data (bytes): The binary content of the PDF file.
        file_name (str): The name of the PDF file.
        mime_type (str): The MIME type of the file, should be 'application/pdf'.

    Returns:
        dict: The JSON content of the response from the WhatsApp API.
    """
    media_id = (await _upload_media(file_data, file_name, mime_type))["id"]
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "document",
        "document": {"filename": file_name, "id": media_id},
    }
    endpoint = f"https://graph.facebook.com/{cfg.WHATSAPP_API_VERSION}/{cfg.WHATSAPP_PHONE_NUMBER_ID}/messages"
    return await _post_httpx_request(endpoint, data=data)

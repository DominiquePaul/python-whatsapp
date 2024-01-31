import typing as t
import json
import os
from functools import wraps
from fastapi import Response, Request, HTTPException
import whatsapp.constants as c
import logging

import whatsapp.utils as wa


def verify(request: Request):
    """
    On webook verification VERIFY_TOKEN has to match the token at the
    configuration and send back "hub.challenge" as success.
    """
    mode = request.query_params.get("hub.mode") == "subscribe"
    challenge = request.query_params.get("hub.challenge")
    token = request.query_params.get("hub.verify_token")

    if mode and challenge:
        if token != os.environ["VERIFY_TOKEN"]:
            return Response(content="Verification token mismatch", status_code=403)
        return Response(content=request.query_params["hub.challenge"])

    return Response(content="Required arguments haven't passed.", status_code=400)


async def process_webhook_data(data: c.WebhookRequestData) -> wa.WamBase | None:
    if data.entry[0].get("changes", [{}])[0].get("value", {}).get("statuses"):
        logging.info("Received a WhatsApp status update.")
        return None
    # if not a status update
    try:
        if wa.is_valid_whatsapp_message(data):
            wam = await wa.parse_whatsapp_message(data)
            return wam
        else:
            # if the request is not a WhatsApp API event, return an error
            raise HTTPException(status_code=404, detail="Not a WhatsApp API event")
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON")
        raise HTTPException(status_code=400, detail="Invalid JSON provided")

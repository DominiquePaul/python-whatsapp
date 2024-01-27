import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import uvicorn
import os
import json

import myapp.constants as c
import myapp.config as cfg
import myapp.whatsapp as wa


load_dotenv()
logging.basicConfig(
    filename="example.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s:%(message)s",
)

# Init App.
app = FastAPI()

# Request Models.


@app.router.get("/api/webhook")
async def verify(request: Request):
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


@app.router.post("/api/webhook")
async def webhook(data: c.WebhookRequestData):
    """
    Messages handler.
    """
    logging.info(data)

    # Check if it's a WhatsApp status update
    if data.entry[0].get("changes", [{}])[0].get("value", {}).get("statuses"):
        logging.info("Received a WhatsApp status update.")
        return JSONResponse(content="ok", status_code=200)

    # if not a status update
    try:
        if wa.is_valid_whatsapp_message(data):
            wam = await wa.parse_whatsapp_message(data)
            if isinstance(wam, wa.WamMediaType):
                await wa.send_message(
                    recipient_id=wam.wa_id, message=f"Mmm, {wam.message_type}"
                )
            elif wam.message_type == "text":
                await wa.send_message(recipient_id=wam.wa_id, message=wam.message_body)

            return JSONResponse(content="ok", status_code=200)
        else:
            # if the request is not a WhatsApp API event, return an error
            response_body = {"status": "error", "message": "Not a WhatsApp API event"}
            return JSONResponse(content=response_body, status_code=404)
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON")
        response_body = {"status": "error", "message": "Invalid JSON provided"}
        return JSONResponse(content=response_body, status_code=400)


if __name__ == "__main__":
    print("your verify token is: ", cfg.VERIFY_TOKEN)
    uvicorn.run("grannymail.main:app", reload=True)

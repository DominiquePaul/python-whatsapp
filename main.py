import json
import logging

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

import whatsapp as wa

load_dotenv()  # needs to happen before cfg is loaded


logging.basicConfig(
    filename="example.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s:%(message)s",
)

# Init App.
app = FastAPI()


@app.router.get("/api/whatsapp")
async def verify(request: Request):
    return wa.verify(request)


@app.router.post("/api/whatsapp")
async def webhook(wam: wa.WamBase = Depends(wa.process_webhook_data)):
    if wam is None:
        return JSONResponse(content="ok", status_code=200)

    if isinstance(wam, wa.WamMediaType):
        await wa.send_message(
            recipient_id=wam.wa_id, message=f"Mmm, {wam.message_type}"
        )
    elif wam.message_type == "text":
        await wa.send_message(recipient_id=wam.wa_id, message=wam.message_body)
    return JSONResponse(content="ok", status_code=200)


if __name__ == "__main__":
    print("your verify token is: ", wa.WHATSAPP_VERIFY_TOKEN)
    uvicorn.run("grannymail.main:app", reload=True)

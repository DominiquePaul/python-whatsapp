import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
import uvicorn

import whatsapp.constants as c
import whatsapp.config as cfg
import whatsapp.utils as wa
import whatsapp.fastapi as wastapi

import json
from fastapi.responses import JSONResponse


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
    return wastapi.verify(request)


# wam: wa.WamBase | None = None # data: c.WebhookRequestData
# , response_model=wa.WamBase
@app.router.post("/api/webhook")
# @wastapi.whatsapp_webhook_decorator
async def webhook(wam: wa.WamBase = Depends(wastapi.process_webhook_data)):
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
    print("your verify token is: ", cfg.VERIFY_TOKEN)
    uvicorn.run("grannymail.main:app", reload=True)

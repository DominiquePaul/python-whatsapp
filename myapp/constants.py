from pydantic import BaseModel


class WebhookRequestData(BaseModel):
    object: str = ""
    entry: list = []

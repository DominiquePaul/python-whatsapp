import pytest

from whatsapp import WebhookRequestData


@pytest.fixture
def example_text_message() -> WebhookRequestData:
    return WebhookRequestData(
        object="whatsapp_business_account",
        entry=[
            {
                "id": "206144975918077",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15551291301",
                                "phone_number_id": "196914110180497",
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Dominique Paul"},
                                    "wa_id": "4915159922222",
                                }
                            ],
                            "messages": [
                                {
                                    "from": "4915159922222",
                                    "id": "wamid.HBgNNDkxNTE1OTkyNjE2MhUCABIYFDNBMDIwQjk1NzQ1ODgxRUI1Njk1AA==",
                                    "timestamp": "1706312529",
                                    "text": {"body": "Hello, this is the message"},
                                    "type": "text",
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    )


@pytest.fixture
def example_text_reply():
    return WebhookRequestData(
        object="whatsapp_business_account",
        entry=[
            {
                "id": "206144975918077",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15551291301",
                                "phone_number_id": "196914110180497",
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Dominique Paul"},
                                    "wa_id": "4915159922222",
                                }
                            ],
                            "messages": [
                                {
                                    "context": {
                                        "from": "15551291301",
                                        "id": "wamid.HBgNNDkxNTE1OTkyNjE2MhUCABIYFDNBMDIwQjk1NzQ1ODgxRUI1Njk1AA==",
                                    },
                                    "from": "4915159922222",
                                    "id": "wamid.HBgNNDkxNTE1OTkyNjE2MhUCABIYFDNBMjVBMTJGQjcwRjM1NkZCNzQ4AA==",
                                    "timestamp": "1706567189",
                                    "text": {
                                        "body": "Hi, my message references the one above"
                                    },
                                    "type": "text",
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    )


@pytest.fixture
def example_voice_message():
    return WebhookRequestData(
        object="whatsapp_business_account",
        entry=[
            {
                "id": "206144975918077",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15551291301",
                                "phone_number_id": "196914110180497",
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Dominique Paul"},
                                    "wa_id": "4915159922222",
                                }
                            ],
                            "messages": [
                                {
                                    "from": "4915159922222",
                                    "id": "wamid.HBgNNDkxNTE1OTkyNjE2MhUCABIYFDNBM0M2MDQ3OEI4RDcxMDMwODE0AA==",
                                    "timestamp": "1706312711",
                                    "type": "audio",
                                    "audio": {
                                        "mime_type": "audio/ogg; codecs=opus",
                                        "sha256": "G1Hj0bsE1u0jOrAronuRexvsU5k+gcGncZCKgbHfcr8=",
                                        "id": "1048715742889904",
                                        "voice": True,
                                    },
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    )


@pytest.fixture
def example_image_message():
    return WebhookRequestData(
        object="whatsapp_business_account",
        entry=[
            {
                "id": "206144975918077",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15551291301",
                                "phone_number_id": "196914110180497",
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Dominique Paul"},
                                    "wa_id": "4915159926263",
                                }
                            ],
                            "messages": [
                                {
                                    "from": "4915159922222",
                                    "id": "wamid.HBgNNDkxNTE1OTkyNjE2MhUCABIYFDNBNUIyN0IzRjE5MUIzREM0Qjc3AA==",
                                    "timestamp": "1706312824",
                                    "type": "image",
                                    "image": {
                                        "mime_type": "image/jpeg",
                                        "sha256": "/EEIcuQqsUpBRW+1KQNd4kTtyhuTYFTI5mTdOwER8Tw=",
                                        "id": "897438572169645",
                                    },
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    )

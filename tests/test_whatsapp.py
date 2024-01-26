from myapp.whatsapp import WamMediaType


def test_WamMediaType():
    wam = WamMediaType(
        message_id="1234",
        wa_id="49151515515",
        profile_name="Dominique Paul",
        message_type="audio",
        timestamp="1705974860",
        mime_type="audio/ogg",
        media_id="23123",
    )

    assert wam.message_body == ""

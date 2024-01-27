import pytest
import myapp.whatsapp as wa


@pytest.mark.asyncio
async def test_parse_whatsapp_message_text(example_text_message):
    result = await wa.parse_whatsapp_message(example_text_message)

    assert result is not None, "The result should not be None"
    assert isinstance(result, wa.WamBase), "The result should be of type WamBase"
    assert (
        result.wa_id == "4915159922222"
    ), "The 'wa_id' value should match the test message sender"
    assert (
        result.message_body == "Hello, this is the message"
    ), "The 'message_body' should contain the message text"


@pytest.mark.asyncio
async def test_parse_voice_message(example_voice_message):
    parsed_message = await wa.parse_whatsapp_message(example_voice_message)

    assert isinstance(
        parsed_message, wa.WamMediaType
    ), "The returned object should be an instance of WamMediaType."
    assert (
        parsed_message.webhook_id == "206144975918077"
    ), "The webhook_id should match the fixture."
    assert (
        parsed_message.message_id
        == "wamid.HBgNNDkxNTE1OTkyNjE2MhUCABIYFDNBM0M2MDQ3OEI4RDcxMDMwODE0AA=="
    ), "The message_id should match the fixture."
    assert (
        parsed_message.phone_number_id == "196914110180497"
    ), "The phone_number_id should match the fixture."
    assert (
        parsed_message.wa_id == "4915159922222"
    ), "The wa_id should match the fixture."
    assert (
        parsed_message.profile_name == "Dominique Paul"
    ), "The profile_name should match the fixture."
    assert parsed_message.message_type == "audio", "The message_type should be 'audio'."
    assert (
        parsed_message.timestamp == "1706312711"
    ), "The timestamp should match the fixture."
    assert (
        parsed_message.mime_type == "audio/ogg; codecs=opus"
    ), "The mime_type should match the fixture."
    assert (
        parsed_message.media_id == "1048715742889904"
    ), "The media_id should match the fixture."
    assert isinstance(
        parsed_message.media_bytes, bytes
    ), "The media_bytes should be of type bytes."


@pytest.mark.asyncio
async def test_parse_image_message(example_image_message):
    parsed_message = await wa.parse_whatsapp_message(example_image_message)

    assert isinstance(
        parsed_message, wa.WamMediaType
    ), "The returned object should be an instance of WamMediaType."
    assert (
        parsed_message.webhook_id == "206144975918077"
    ), "The webhook_id should match the fixture."
    assert (
        parsed_message.message_id
        == "wamid.HBgNNDkxNTE1OTkyNjE2MhUCABIYFDNBNUIyN0IzRjE5MUIzREM0Qjc3AA=="
    ), "The message_id should match the fixture."
    assert (
        parsed_message.phone_number_id == "196914110180497"
    ), "The phone_number_id should match the fixture."
    assert (
        parsed_message.wa_id == "4915159926263"
    ), "The wa_id should match the fixture."
    assert (
        parsed_message.profile_name == "Dominique Paul"
    ), "The profile_name should match the fixture."
    assert parsed_message.message_type == "image", "The message_type should be 'image'."
    assert (
        parsed_message.timestamp == "1706312824"
    ), "The timestamp should match the fixture."
    assert (
        parsed_message.mime_type == "image/jpeg"
    ), "The mime_type should match the fixture."
    assert (
        parsed_message.media_id == "897438572169645"
    ), "The media_id should match the fixture."
    assert isinstance(
        parsed_message.media_bytes, bytes
    ), "The media_bytes should be of type bytes."

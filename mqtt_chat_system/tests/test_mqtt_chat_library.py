from json import loads
from datetime import datetime
from mqtt_chat_system.mqtt_chat_library import create_message


def test_create_message_content():
    # Call function
    message = loads((create_message("Test content", "test_sender")))

    # Test
    assert message["content"] == "Test content"


def test_create_message_sender():
    # Call the function
    message = loads((create_message("Test content", "test_sender")))

    # Test
    assert message["sender"] == "test_sender"


def test_create_message_timestamp():
    # Call function
    message = loads((create_message("Test content", "test_sender")))

    # Process result from function
    now = datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
    message_creation_time = datetime.strptime(message["timestamp"], "%H:%M:%S")

    # Tests
    assert (now - message_creation_time).total_seconds() < 2

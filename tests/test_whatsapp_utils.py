"""
Unit tests for WhatsApp utility functions
"""
import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.whatsapp_utils import (
    get_text_message_input,
    get_template_message_input,
    process_text_for_whatsapp,
    is_valid_whatsapp_message
)


class TestWhatsAppUtils(unittest.TestCase):
    """Test cases for WhatsApp utility functions"""

    def test_get_text_message_input_structure(self):
        """Test that text message has correct structure"""
        recipient = "1234567890"
        text = "Hello, World!"
        result = get_text_message_input(recipient, text)
        data = json.loads(result)

        self.assertEqual(data["messaging_product"], "whatsapp")
        self.assertEqual(data["to"], recipient)
        self.assertEqual(data["type"], "text")
        self.assertEqual(data["text"]["body"], text)

    def test_get_template_message_input_without_image(self):
        """Test template message structure without image"""
        recipient = "1234567890"
        template_name = "test_template"
        result = get_template_message_input(recipient, template_name)
        data = json.loads(result)

        self.assertEqual(data["messaging_product"], "whatsapp")
        self.assertEqual(data["to"], recipient)
        self.assertEqual(data["type"], "template")
        self.assertEqual(data["template"]["name"], template_name)
        self.assertEqual(data["template"]["language"]["code"], "es")

    def test_get_template_message_input_with_image(self):
        """Test template message structure with image header"""
        recipient = "1234567890"
        template_name = "test_template"
        image_url = "https://example.com/image.jpg"
        result = get_template_message_input(
            recipient,
            template_name,
            header_image_url=image_url
        )
        data = json.loads(result)

        self.assertEqual(data["messaging_product"], "whatsapp")
        self.assertEqual(data["to"], recipient)
        self.assertEqual(data["type"], "template")
        self.assertEqual(data["template"]["name"], template_name)
        self.assertIn("components", data["template"])
        self.assertEqual(data["template"]["components"][0]["type"], "header")
        self.assertEqual(
            data["template"]["components"][0]["parameters"][0]["image"]["link"],
            image_url
        )

    def test_get_template_message_input_custom_language(self):
        """Test template message with custom language code"""
        recipient = "1234567890"
        template_name = "test_template"
        language = "en"
        result = get_template_message_input(recipient, template_name, language_code=language)
        data = json.loads(result)

        self.assertEqual(data["template"]["language"]["code"], language)

    def test_process_text_for_whatsapp_removes_brackets(self):
        """Test that text processing removes special brackets"""
        text = "Hello 【source】 World"
        result = process_text_for_whatsapp(text)
        self.assertNotIn("【", result)
        self.assertNotIn("】", result)

    def test_process_text_for_whatsapp_converts_markdown(self):
        """Test that double asterisks are converted to single"""
        text = "This is **bold** text"
        result = process_text_for_whatsapp(text)
        self.assertEqual(result, "This is *bold* text")

    def test_process_text_for_whatsapp_multiple_bold(self):
        """Test multiple bold conversions"""
        text = "**First** and **Second** bold"
        result = process_text_for_whatsapp(text)
        self.assertEqual(result, "*First* and *Second* bold")

    def test_is_valid_whatsapp_message_valid(self):
        """Test validation of a valid WhatsApp message"""
        valid_message = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "messages": [
                                    {
                                        "from": "1234567890",
                                        "text": {"body": "Hello"}
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
        self.assertTrue(is_valid_whatsapp_message(valid_message))

    def test_is_valid_whatsapp_message_missing_object(self):
        """Test validation fails when object is missing"""
        invalid_message = {
            "entry": [{"changes": [{"value": {"messages": [{}]}}]}]
        }
        self.assertFalse(is_valid_whatsapp_message(invalid_message))

    def test_is_valid_whatsapp_message_missing_messages(self):
        """Test validation fails when messages are missing"""
        invalid_message = {
            "object": "whatsapp_business_account",
            "entry": [{"changes": [{"value": {}}]}]
        }
        self.assertFalse(is_valid_whatsapp_message(invalid_message))

    def test_is_valid_whatsapp_message_empty_body(self):
        """Test validation with empty body"""
        empty_body = {}
        self.assertFalse(is_valid_whatsapp_message(empty_body))


class TestMessageFormatting(unittest.TestCase):
    """Test cases for message formatting"""

    def test_text_message_json_format(self):
        """Test that text message is valid JSON"""
        result = get_text_message_input("1234567890", "Test")
        try:
            json.loads(result)
            valid_json = True
        except json.JSONDecodeError:
            valid_json = False
        self.assertTrue(valid_json)

    def test_template_message_json_format(self):
        """Test that template message is valid JSON"""
        result = get_template_message_input("1234567890", "test_template")
        try:
            json.loads(result)
            valid_json = True
        except json.JSONDecodeError:
            valid_json = False
        self.assertTrue(valid_json)


if __name__ == '__main__':
    unittest.main()

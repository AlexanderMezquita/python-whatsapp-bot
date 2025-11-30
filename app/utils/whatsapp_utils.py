import logging
from flask import current_app, jsonify
import json
import requests
import re
import time

# from app.services.openai_service import generate_response
from app.utils.message_handlers import (
    generate_response,
    get_welcome_message,
    should_send_welcome,
)


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def get_template_message_input(recipient, template_name, language_code="es", header_image_url=None):
    template_data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code}
        },
    }

    # Add header component if image URL is provided
    if header_image_url:
        template_data["template"]["components"] = [
            {
                "type": "header",
                "parameters": [
                    {
                        "type": "image",
                        "image": {
                            "link": header_image_url
                        }
                    }
                ]
            }
        ]

    return json.dumps(template_data)


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        # Log the actual error response from WhatsApp API
        if hasattr(e, 'response') and e.response is not None:
            logging.error(f"WhatsApp API Error Response: {e.response.text}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    # Check if this is a new user and send welcome messages
    if should_send_welcome(wa_id):
        logging.info(f"Sending welcome messages to new user: {wa_id}")

        # Send template message first with header image
        header_image_url = "https://www.rizosafrosymas.com/_next/image?url=%2Fram1.jpg&w=2048&q=75"
        template_data = get_template_message_input(
            wa_id,
            "mensaje_de_bienvenida",
            header_image_url=header_image_url
        )
        template_response = send_message(template_data)

        # Log template response for debugging
        if isinstance(template_response, tuple):
            logging.error(f"Template message failed: {template_response}")
        else:
            logging.info(f"Template message response: {template_response.status_code} - {template_response.text}")

        # Wait a bit to ensure template is delivered first
        time.sleep(2)

        # Then send text welcome message with menu
        welcome_message = get_welcome_message()
        welcome_data = get_text_message_input(wa_id, welcome_message)
        send_message(welcome_data)

    # Generate response to user's message
    response = generate_response(message_body)

    # OpenAI Integration
    # response = generate_response(message_body, wa_id, name)
    # response = process_text_for_whatsapp(response)

    data = get_text_message_input(wa_id, response)
    send_message(data)


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )

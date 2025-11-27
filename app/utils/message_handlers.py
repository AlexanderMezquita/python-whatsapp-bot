"""
Message handlers for WhatsApp bot responses
"""
import os

# Track users who have already received the welcome message
greeted_users = set()

# Path to messages directory
MESSAGES_DIR = os.path.join(os.path.dirname(__file__), 'messages')


def load_message(filename):
    """
    Load a message from a text file.

    Args:
        filename (str): Name of the message file (without path)

    Returns:
        str: The message content
    """
    file_path = os.path.join(MESSAGES_DIR, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return f"Error: Message file '{filename}' not found."


def get_welcome_message():
    """
    Returns the welcome message that is sent when a user first contacts the bot.

    Returns:
        str: The welcome message
    """
    return load_message('welcome.txt')


def should_send_welcome(wa_id):
    """
    Check if a user should receive the welcome message.

    Args:
        wa_id (str): WhatsApp ID of the user

    Returns:
        bool: True if welcome message should be sent
    """
    if wa_id not in greeted_users:
        greeted_users.add(wa_id)
        return True
    return False


def generate_response(response):
    """
    Generate a response based on keywords in the incoming message.

    Args:
        response (str): The incoming message from the user

    Returns:
        str: The appropriate response based on keywords
    """
    # Normalize the message to lowercase for comparison
    message_lower = response.lower().strip()

    # Keyword-based responses using if/else
    if "consulta capilar" in message_lower or "consulta" in message_lower or "relajacion" in message_lower or "relajación" in message_lower:
        return load_message('consulta_capilar.txt')
    elif "wash and go" in message_lower or "lavado" in message_lower or "definicion de rizos" in message_lower or "definición de rizos" in message_lower:
        return load_message('lavado_rizos.txt')
    elif "rizos elaborados" in message_lower or "elaborados" in message_lower or "flexis" in message_lower:
        return load_message('rizos_elaborados.txt')
    elif "trenzas" in message_lower or "boxbraids" in message_lower or "box braids" in message_lower or "africanas" in message_lower:
        return load_message('trenzas_africanas.txt')
    elif "crochet" in message_lower or "metodo crochet" in message_lower or "método crochet" in message_lower:
        return load_message('metodo_crochet.txt')
    elif "prueba de color" in message_lower or "prueba color" in message_lower or ("prueba" in message_lower and "color" in message_lower):
        return load_message('prueba_color.txt')
    elif "color" in message_lower or "tinte" in message_lower:
        return load_message('color_hint.txt')
    elif "costos" in message_lower:
        return load_message('costos.txt')
    elif "horario" in message_lower:
        return load_message('horario.txt')
    elif "servicios" in message_lower:
        return load_message('servicios.txt')
    elif "ubicacion" in message_lower or "ubicación" in message_lower:
        return load_message('ubicacion.txt')
    elif "reserva" in message_lower:
        return load_message('reserva.txt')
    elif "hola" in message_lower:
        return load_message('hola.txt')
    elif "gracias" in message_lower:
        return load_message('gracias.txt')
    else:
        # Default response if no keyword matches
        return f"Recibí tu mensaje: '{response}'. ¿Puedes ser más específico? Escribe 'servicios' para ver lo que ofrecemos."

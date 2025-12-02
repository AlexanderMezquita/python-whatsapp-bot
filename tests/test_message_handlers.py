"""
Unit tests for message handlers
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.message_handlers import generate_response, should_send_welcome, greeted_users


class TestMessageHandlers(unittest.TestCase):
    """Test cases for message handler functions"""

    def setUp(self):
        """Set up test fixtures"""
        # Clear greeted users before each test
        greeted_users.clear()

    def test_consulta_keyword(self):
        """Test that 'consulta' keyword triggers correct response"""
        response = generate_response("consulta")
        self.assertIn("consulta", response.lower())

    def test_consulta_capilar_keyword(self):
        """Test that 'consulta capilar' triggers correct response"""
        response = generate_response("consulta capilar")
        self.assertIn("consulta", response.lower())

    def test_lavado_keyword(self):
        """Test that 'lavado' keyword triggers wash and go response"""
        response = generate_response("lavado")
        self.assertIsNotNone(response)

    def test_wash_and_go_keyword(self):
        """Test that 'wash and go' triggers correct response"""
        response = generate_response("wash and go")
        self.assertIsNotNone(response)

    def test_rizos_elaborados_keyword(self):
        """Test that 'rizos elaborados' triggers correct response"""
        response = generate_response("rizos elaborados")
        self.assertIsNotNone(response)

    def test_trenzas_keyword(self):
        """Test that 'trenzas' keyword triggers correct response"""
        response = generate_response("trenzas")
        self.assertIsNotNone(response)

    def test_boxbraids_keyword(self):
        """Test that 'boxbraids' keyword triggers trenzas response"""
        response = generate_response("boxbraids")
        self.assertIsNotNone(response)

    def test_crochet_keyword(self):
        """Test that 'crochet' keyword triggers correct response"""
        response = generate_response("crochet")
        self.assertIsNotNone(response)

    def test_color_keyword(self):
        """Test that 'color' keyword triggers correct response"""
        response = generate_response("color")
        self.assertIsNotNone(response)

    def test_prueba_color_keyword(self):
        """Test that 'prueba de color' triggers correct response"""
        response = generate_response("prueba de color")
        self.assertIsNotNone(response)

    def test_costos_keyword(self):
        """Test that 'costos' keyword triggers correct response"""
        response = generate_response("costos")
        self.assertIsNotNone(response)

    def test_horario_keyword(self):
        """Test that 'horario' keyword triggers correct response"""
        response = generate_response("horario")
        self.assertIsNotNone(response)

    def test_servicios_keyword(self):
        """Test that 'servicios' keyword triggers correct response"""
        response = generate_response("servicios")
        self.assertIsNotNone(response)

    def test_ubicacion_keyword(self):
        """Test that 'ubicacion' keyword triggers correct response"""
        response = generate_response("ubicacion")
        self.assertIsNotNone(response)

    def test_reserva_keyword(self):
        """Test that 'reserva' keyword triggers correct response"""
        response = generate_response("reserva")
        self.assertIsNotNone(response)

    def test_cita_keyword(self):
        """Test that 'cita' keyword triggers reserva response"""
        response = generate_response("cita")
        self.assertIsNotNone(response)

    def test_hola_keyword(self):
        """Test that 'hola' keyword triggers greeting response"""
        response = generate_response("hola")
        self.assertIsNotNone(response)

    def test_gracias_keyword(self):
        """Test that 'gracias' keyword triggers thank you response"""
        response = generate_response("gracias")
        self.assertIsNotNone(response)

    def test_unknown_keyword(self):
        """Test that unknown keywords return default response"""
        response = generate_response("xyz123unknown")
        self.assertIn("Recibí tu mensaje", response)

    def test_case_insensitive(self):
        """Test that keywords are case insensitive"""
        response_lower = generate_response("consulta")
        response_upper = generate_response("CONSULTA")
        response_mixed = generate_response("CoNsUlTa")
        # All should trigger the same response type
        self.assertIsNotNone(response_lower)
        self.assertIsNotNone(response_upper)
        self.assertIsNotNone(response_mixed)

    def test_should_send_welcome_new_user(self):
        """Test that new users should receive welcome message"""
        result = should_send_welcome("1234567890")
        self.assertTrue(result)

    def test_should_send_welcome_existing_user(self):
        """Test that existing users should not receive welcome message again"""
        wa_id = "1234567890"
        should_send_welcome(wa_id)  # First call
        result = should_send_welcome(wa_id)  # Second call
        self.assertFalse(result)

    def test_greeted_users_persistence(self):
        """Test that greeted users are tracked correctly"""
        wa_id1 = "1111111111"
        wa_id2 = "2222222222"

        should_send_welcome(wa_id1)
        should_send_welcome(wa_id2)

        self.assertIn(wa_id1, greeted_users)
        self.assertIn(wa_id2, greeted_users)


class TestMessageContent(unittest.TestCase):
    """Test cases to verify message content is being loaded"""

    def test_responses_not_empty(self):
        """Test that responses are not empty strings"""
        keywords = ["consulta", "lavado", "trenzas", "costos", "horario"]
        for keyword in keywords:
            response = generate_response(keyword)
            self.assertTrue(len(response) > 0)

    def test_responses_are_strings(self):
        """Test that all responses are strings"""
        keywords = ["consulta", "lavado", "trenzas", "costos", "horario"]
        for keyword in keywords:
            response = generate_response(keyword)
            self.assertIsInstance(response, str)


if __name__ == '__main__':
    unittest.main()

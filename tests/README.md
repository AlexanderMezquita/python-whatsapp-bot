# WhatsApp Bot Test Suite

This directory contains unit tests for the WhatsApp bot application.

## Test Files

- `test_message_handlers.py` - Tests for message handling and keyword responses
- `test_whatsapp_utils.py` - Tests for WhatsApp utility functions

## Running Tests

### Run all tests
```bash
python -m pytest tests/
```

Or using unittest:
```bash
python -m unittest discover tests/
```

### Run specific test file
```bash
python -m pytest tests/test_message_handlers.py
```

Or:
```bash
python tests/test_message_handlers.py
```

### Run with coverage
```bash
python -m pytest --cov=app tests/
```

## Test Coverage

The test suite covers:

### Message Handlers (`test_message_handlers.py`)
- ✅ Keyword detection (consulta, lavado, trenzas, etc.)
- ✅ Case-insensitive matching
- ✅ Welcome message logic
- ✅ Greeted users tracking
- ✅ Default/unknown keyword responses

### WhatsApp Utils (`test_whatsapp_utils.py`)
- ✅ Text message formatting
- ✅ Template message formatting (with and without images)
- ✅ Message validation
- ✅ Text processing (markdown conversion, bracket removal)
- ✅ JSON structure validation

## Adding New Tests

When adding new features to the bot:

1. Create test cases in the appropriate test file
2. Follow the existing naming convention: `test_<feature_name>`
3. Use descriptive docstrings
4. Run tests before committing changes

## Example Test

```python
def test_new_keyword(self):
    """Test that 'new_keyword' triggers correct response"""
    response = generate_response("new_keyword")
    self.assertIn("expected text", response.lower())
```

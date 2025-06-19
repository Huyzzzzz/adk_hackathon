"""Data Objects Agent prompts."""

DATA_OBJECTS_PROMPT = """Identify and model all data entities from user requirements.

Create detailed data objects with attributes, relationships, and business rules.

User Requirements:
{user_requirements_extraction}
"""

DATA_OBJECTS_EXTRACTION_PROMPT = """Extract and structure the data objects analysis from the following content.

Extract and return only the structured data objects information in clean JSON format."""

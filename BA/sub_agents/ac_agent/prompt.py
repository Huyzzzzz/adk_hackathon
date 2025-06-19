"""Actors Agent prompts."""

ACTORS_PROMPT = """Identify all actors and stakeholders from user requirements.

Create detailed actor profiles with roles, responsibilities, and interactions.

User Requirements:
{user_requirements_extraction}

"""

ACTORS_EXTRACTION_PROMPT = """Extract and structure the actors analysis from the following content.


Extract and return only the structured actors information in clean JSON format."""

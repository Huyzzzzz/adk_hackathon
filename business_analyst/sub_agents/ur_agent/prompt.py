"""User Requirements Agent prompts."""

USER_REQUIREMENTS_PROMPT = """Extract structured user requirements from business documents.

Analyze documents and identify all functional and non-functional requirements from {business_analyst_output}.

"""

USER_REQUIREMENTS_EXTRACTION_PROMPT = """Extract and structure the user requirements analysis from the following content.

Extract and return only the structured user requirements information in clean JSON format."""
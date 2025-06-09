"""Use Cases Agent prompts."""

USE_CASES_PROMPT = """Create comprehensive use cases integrating all business analysis components.

Define use cases with actors, flows, and data object interactions.

User Requirements:
{user_requirements_extraction}

Actors Analysis:
{ac_agent_output}

Data Objects Analysis:
{do_agent_output}

"""

USE_CASES_EXTRACTION_PROMPT = """Extract and structure the use cases analysis from the following content.

Extract and return only the structured use cases information in clean JSON format."""

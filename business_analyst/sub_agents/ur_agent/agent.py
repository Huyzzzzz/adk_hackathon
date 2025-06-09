"""
The User Requirement (UR) Generation Agent.
"""

from typing import List
from google.adk import Agent
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig


class UserRequirement(BaseModel):
    """Structure for a user requirement."""
    id: str = Field(description="Unique identifier for the requirement")
    name: str = Field(description="Clear, descriptive requirement name")
    source: str = Field(description="Where the requirement originated")
    type: str = Field(description="Type of requirement (functional, business rule, constraint, etc.)")
    detail: str = Field(description="Detailed description with acceptance criteria")
    covered_usr: str = Field(description="Related user stories or requirements")

class UserRequirementsOutput(BaseModel):
    """Output structure for user requirements analysis."""
    requirements: List[UserRequirement] = Field(description="List of extracted user requirements")

# TODO: Define tool in here
def parse_file():
    pass

# Create the User Requirements Agent with LLM reasoning-based tools
ur_extraction = Agent(
    model="gemini-2.5-flash-preview-05-20",
    name="user_requirements_extraction",
    instruction=
    """
    Extract the user requirements based on the given content.
    """,
    output_schema=UserRequirementsOutput, 
    output_key="user_requirements_output",
)

ur_agent = Agent(
    model="gemini-2.5-flash-preview-05-20",
    name="user_requirements_agent",
    description="An agent that extracts user requirements from a given content",
    instruction=
    """
    Extract the user requirements based on the given content.
    """,
    tools=[
        AgentTool(agent=ur_extraction),
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.0, top_p=0.5
    )
)



"""
The User Requirement (UR) Generation Agent.
"""

from typing import List
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

from .prompt import USER_REQUIREMENTS_PROMPT, USER_REQUIREMENTS_EXTRACTION_PROMPT
from ...utils.utils import get_env_var


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

# Create the User Requirements Agent with LLM reasoning-based tools
ur_extraction = LlmAgent(
    model=get_env_var("UR_AGENT_MODEL"),
    name="user_requirements_extraction",
    instruction=USER_REQUIREMENTS_EXTRACTION_PROMPT,
    output_schema=UserRequirementsOutput, 
    output_key="user_requirements_extraction",
)

ur_agent = LlmAgent(
    model=get_env_var("UR_AGENT_MODEL"),
    name="ur_agent",
    instruction=USER_REQUIREMENTS_PROMPT,
    tools=[
        AgentTool(agent=ur_extraction)
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.0,
        top_p=0.5
    )
)

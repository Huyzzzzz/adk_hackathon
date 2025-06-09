"""
The Actors (AC) Generation Agent.
"""

from typing import List
from google.adk import Agent
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

from .prompt import ACTORS_PROMPT, ACTORS_EXTRACTION_PROMPT
from ...utils.utils import get_env_var


class ActorInteraction(BaseModel):
    """Structure for actor interactions."""
    target: str = Field(description="Who or what the actor interacts with")
    interaction_type: str = Field(description="Type of interaction (uses, manages, reports to, etc.)")
    description: str = Field(description="Description of the interaction")


class Actor(BaseModel):
    """Structure for an actor."""
    id: str = Field(description="Unique identifier for the actor")
    name: str = Field(description="Actor name or role title")
    role: str = Field(description="Primary role or responsibility")
    responsibilities: List[str] = Field(description="Detailed list of what they do")
    permissions: List[str] = Field(description="Access rights and capabilities")
    interactions: List[ActorInteraction] = Field(description="How they interact with the system and other actors")


class ActorsOutput(BaseModel):
    """Output structure for actors analysis."""
    actors: List[Actor] = Field(description="List of identified actors")
    actor_hierarchy: str = Field(description="Description of actor relationships and hierarchy")
    stakeholder_summary: str = Field(description="Summary of stakeholder analysis")


# TODO: Define tool in here
def parse_actors():
    pass

# Create the Actors extraction Agent with LLM reasoning-based tools
ac_extraction = Agent(
    model=get_env_var("AC_AGENT_MODEL"),
    name="actors_extraction",
    instruction=ACTORS_EXTRACTION_PROMPT,
    output_schema=ActorsOutput,
    output_key="ac_agent_output",
)

ac_agent = Agent(
    model=get_env_var("AC_AGENT_MODEL"),
    name="ac_agent",
    # description="Identifies actors and stakeholders from requirements analysis",
    instruction=ACTORS_PROMPT,
    tools=[
        AgentTool(agent=ac_extraction),
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.0, top_p=0.5
    )
)

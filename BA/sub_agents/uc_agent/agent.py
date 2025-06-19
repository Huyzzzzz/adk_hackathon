"""
The Use Cases (UC) Generation Agent.
"""

from typing import List, Optional
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

from .prompt import USE_CASES_PROMPT, USE_CASES_EXTRACTION_PROMPT
from ...utils.utils import get_env_var


# class UseCaseStep(BaseModel):
#     """Structure for a use case step."""
#     step_number: int = Field(description="Step sequence number")
#     actor_action: str = Field(description="What the actor does")
#     system_response: str = Field(description="How the system responds")
#     notes: Optional[str] = Field(description="Additional notes or alternatives")


# class UseCaseScenario(BaseModel):
#     """Structure for a use case scenario."""
#     scenario_type: str = Field(description="Type of scenario (main, alternative, exception)")
#     name: str = Field(description="Scenario name")
#     steps: List[UseCaseStep] = Field(description="Sequence of steps in the scenario")
#     trigger: str = Field(description="What triggers this scenario")


class UseCase(BaseModel):
    """Structure for a use case."""
    id: str = Field(description="Unique identifier for the use case")
    name: str = Field(description="Use case name")
    actors: List[str] = Field(description="Primary and secondary actors involved")
    description: str = Field(description="Purpose and business value")
    preconditions: List[str] = Field(description="What must be true before execution")
    postconditions: List[str] = Field(description="Expected outcomes and state changes")
    # scenarios: List[UseCaseScenario] = Field(description="Step-by-step flows (main and alternative)")


class UseCasesOutput(BaseModel):
    """Output structure for use cases analysis."""
    use_cases: List[UseCase] = Field(description="List of identified use cases")
    # use_case_diagram_description: str = Field(description="Description of how use cases relate to each other")
    # coverage_analysis: str = Field(description="Analysis of requirement coverage by use cases")


# Create the Use Cases extraction Agent with LLM reasoning-based tools
uc_extraction = LlmAgent(
    model=get_env_var("UC_AGENT_MODEL"),
    name="use_cases_extraction",
    instruction=USE_CASES_EXTRACTION_PROMPT,
    output_schema=UseCasesOutput,
    output_key="uc_agent_output",
)

uc_agent = LlmAgent(
    model=get_env_var("UC_AGENT_MODEL"),
    name="uc_agent",
    instruction=USE_CASES_PROMPT,
    tools=[
        AgentTool(agent=uc_extraction),
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.0, 
        top_p=0.5
    )
)

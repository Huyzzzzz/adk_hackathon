"""
The Data Objects (DO) Generation Agent.
"""

from typing import List
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

from .prompt import DATA_OBJECTS_PROMPT, DATA_OBJECTS_EXTRACTION_PROMPT
from ...utils.utils import get_env_var


# class DataProperty(BaseModel):
#     """Structure for a data object property."""
#     name: str = Field(description="Property name")
#     type: str = Field(description="Data type (string, integer, boolean, etc.)")
#     required: bool = Field(description="Whether the property is required")
#     description: str = Field(description="Description of the property")
#     constraints: List[str] = Field(description="Validation rules and constraints")



class DataObject(BaseModel):
    """Structure for a data object."""
    id: str = Field(description="Unique identifier for the data object")
    name: str = Field(description="Entity name")
    description: str = Field(description="Purpose and business meaning")
    # properties: List[DataProperty] = Field(description="List of attributes with types and constraints")
    # constraints: List[str] = Field(description="Business rules and validation requirements")


class DataObjectsOutput(BaseModel):
    """Output structure for data objects analysis."""
    data_objects: List[DataObject] = Field(description="List of identified data objects")
    # data_model_summary: str = Field(description="Summary of the overall data model")


# Create the Data Objects extraction Agent with LLM reasoning-based tools
do_extraction = LlmAgent(
    model=get_env_var("DO_AGENT_MODEL"),
    name="data_objects_extraction", 
    instruction=DATA_OBJECTS_EXTRACTION_PROMPT,
    output_schema=DataObjectsOutput,
    output_key="do_agent_output",
)

do_agent = LlmAgent(
    model=get_env_var("DO_AGENT_MODEL"),
    name="do_agent",
    instruction=DATA_OBJECTS_PROMPT,
    tools=[
        AgentTool(agent=do_extraction),
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.0, 
        top_p=0.5
    )
)

import json
from pydantic import BaseModel, Field
from google.adk.agents import Agent

def hello(name: str) -> str:
    return f"Hello {name}!"

class UserRequirement(BaseModel):
    name: str = Field(description="A short overview description summarizing the requirement.")
    source: str = Field(description="The filename from which the requirement was extracted.")
    detail: str = Field(description="A detailed explanation of what the user needs to do.")
    covered_usr: str = Field(description="Yes or No – whether this requirement is likely already covered by another requirement.")


root_agent = Agent(
    name="hello_agent",
    model="gemini-2.0-flash",
    description="A user requirement agent.",
    instruction=
    """
    You are an expert assistant trained to extract user requirements from Request for Proposal (RFP) or Request for Information (RFI) documents. Your task is to analyze long and complex documents and extract relevant user requirements in a structured format.
    Your task is from the uploaded RFP/RFI file, identify all User Requirements that describe what a user needs to do with a system, product, or service to achieve a specific goal. For each user requirement you extract, provide the following fields:
    Output Schema:
    {json.dumps(UserRequirement.model_json_schema(), indent=2)}
    """,
    output_schema=UserRequirement,
)
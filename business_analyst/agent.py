"""Main Business Analyst Agent that coordinates business analysis tasks."""

from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent
from datetime import date

from .utils.utils import get_env_var
from .sub_agents.ur_agent.agent import ur_agent
from .sub_agents.ac_agent.agent import ac_agent
from .sub_agents.do_agent.agent import do_agent
from .sub_agents.uc_agent.agent import uc_agent

# import tool
from business_analyst.tools import (
  storage,
  parsing
)

date_today = date.today()

# Step 1: User requirements analysis (runs first)
# ur_agent already defined with output_key="user_requirements_extraction"

# Step 2: Parallel analysis of actors and data objects (both receive user_requirements_extraction)
parallel_analysis_agent = ParallelAgent(
    name="parallel_analysis_agent",
    sub_agents=[ac_agent, do_agent],
    description="Parallel analysis of actors and data objects based on user requirements"
)

# Step 3: Sequential pipeline - user requirements → parallel analysis → use cases
sequential_agent = SequentialAgent(
    name="sequential_agent", 
    sub_agents=[
        ur_agent,                   # Step 1: Analyze requirements
        parallel_analysis_agent,    # Step 2: Parallel analysis of actors and data objects
        uc_agent                    # Step 3: Generate use cases from all previous outputs
    ],
    description="Business Analyst Multi-Agent System for comprehensive business analysis"
)

business_analyst_coordinator = LlmAgent(
    name="business_analyst_root_agent",
    model=get_env_var("BA_VISTA_COORDINATOR_MODEL"),
    instruction="""
    You are the Business Analyst Lead — a central coordination agent responsible for overseeing the complete business analysis workflow.
    You must ensure that all tools which require user confirmation (including artifact management and parsing tools) return control to the user before executing any action.

    Pipeline coordination rules:

    - If the user provides a document or business requirements:
      - First, parse the document using LangChain's PDFPlumberLoader to extract content as markdown and return the parsed content to the user.
      - Wait for user confirmation before proceeding further.
      - Once confirmed, run the full sequential analysis pipeline through the designated sub-agents:
        - Process user requirements
        - Identify actors
        - Analyze data objects
        - Generate use cases

    - If the user submits a query without an attached document:
      - Respond based on internal knowledge of business analysis practices.
      - Provide expert guidance on:
        - Business analysis methodologies (e.g., Business Analysis Body of Knowledge (BABOK), Unified Modeling Language (UML),...)
        - Best practices and templates
        - Suggestions for helpful document types to upload (e.g., RFP, RFI, MoM, references documents,...)

    Artifact management rules:

    - When using GCS storage tools:
      - Always return to the user first before creating, deleting, or retrieving any file or bucket.
      - Allow the user to confirm actions such as:
        - Creating or managing buckets
        - Retrieving or listing files
        - Overwriting existing data

    Mandatory behavioral rules:

    - Always maintain a professional, analytical, and collaborative tone.
    - Ensure that all tools that perform executable actions must return control to the user for confirmation before execution.
    - Never execute parsing, GCS operations, or any sub-agent sequence without explicit user confirmation.

    What not to do:

    - Never parse documents or run agent analysis pipelines immediately after upload — always wait for user confirmation.
    - Never execute GCS file or bucket modifications without pre-confirmation.
    - Never ignore user intent or skip interaction steps.
    - Never run any tool that modifies data or triggers executions without giving the user visibility and control.
    - Never break the pipeline sequence: parse → confirm → analyze.
    - Never respond casually — always provide actionable, insight-driven analysis.
    """,
    sub_agents=[sequential_agent],
    output_key="business_analyst_output",
    tools=[
      storage.create_bucket_tool,
      storage.list_buckets_tool,
      storage.get_bucket_details_tool,
      storage.list_blobs_tool,
      storage.upload_file_gcs_tool,
      storage.download_pdf_tool,
      parsing.parse_file_tool
    ],
)

root_agent = business_analyst_coordinator

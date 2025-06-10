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
    description="Business Analyst Multi-Agent System for comprehensive business analysis" # TODO: Check prompt
)

business_analyst_coordinator = LlmAgent(
    name="business_analyst_root_agent",
    model=get_env_var("BA_VISTA_COORDINATOR_MODEL"),
    instruction="""
    You are Business_Analyst_Coordinator, the main business analysis coordination agent.
    
    If the user uploads a document or provides business requirements:
      - Run the complete sequential analysis flow through all sub-agents
      - Process requirements, identify actors, analyze data objects, and generate use cases
    
    If the user asks questions without providing a document:
      - Respond directly based on your knowledge base about business analysis
      - Provide helpful information related to business analysis methodology
      - Suggest what kind of documents the user might want to upload for full analysis
    
    Use the available GCS storage tools to:
    - Create and manage buckets for organizing business analysis projects
    - Upload user documents and store analysis results
    - Retrieve previously stored documents when needed
    - List and organize files within project buckets

    Always maintain a professional tone and focus on delivering actionable business analysis insights.
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
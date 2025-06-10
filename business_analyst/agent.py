"""Main Business Analyst Agent that coordinates business analysis tasks."""
from pathlib import Path
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent
from datetime import date
from .utils.utils import get_env_var
from .sub_agents.ur_agent.agent import ur_agent
from .sub_agents.ac_agent.agent import ac_agent
from .sub_agents.do_agent.agent import do_agent
from .sub_agents.uc_agent.agent import uc_agent
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.tools import FunctionTool
from .tools.markdown import convert_and_save_json
from pathlib import Path
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
add_tool = FunctionTool(
    func=convert_and_save_json,
    description="Convert and save the current agent state to a markdown file",
    name="save_state_to_markdown"
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
    Before the session end, you must use the `add_tool` function to save all the outputs and inputs to markdown format.
    Always maintain a professional tone and focus on delivering actionable business analysis insights.
    """,
    sub_agents=[sequential_agent],
    tools=[add_tool],
    output_key="business_analyst_output",
)

root_agent = business_analyst_coordinator



# APP_NAME = "BA VISTA"
# USER_ID="user1234"
# SESSION_ID="1234"
# db_path = Path(__file__).parent / "my_agent_data.db"
# db_url = f"sqlite:///{db_path.as_posix()}"
# session_service = DatabaseSessionService(db_url=db_url)
# runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
# def call_agent(query):
#     content = types.Content(role='user', parts=[types.Part(text=query)])
#     events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

#     for event in events:
#         if event.is_final_response():
#             final_response = event.content.parts[0].text
#             print("Agent Response: ", final_response)

# call_agent()


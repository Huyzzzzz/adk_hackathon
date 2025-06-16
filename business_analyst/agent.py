"""Main Business Analyst Agent that coordinates business analysis tasks."""
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent
from .utils.utils import get_env_var
from .sub_agents.ur_agent.agent import ur_agent
from .sub_agents.ac_agent.agent import ac_agent
from .sub_agents.do_agent.agent import do_agent
from .sub_agents.uc_agent.agent import uc_agent
from .tools.file import read_file_tool, find_file_tool, save_input_tool
from .tools.save_agent_ouput import save_actors_ouput_tool, save_data_objects_ouput_tool, save_use_cases_ouput_tool, save_user_requirements_ouput_tool


parallel_analysis_agent = ParallelAgent(
    name="parallel_analysis_agent",
    sub_agents=[ac_agent, do_agent],
    description="Parallel analysis of actors and data objects based on user requirements"
)


sequential_agent = SequentialAgent(
    name="sequential_agent", 
    sub_agents=[
        ur_agent,
        parallel_analysis_agent,
        uc_agent,
    ],
    description="Business Analyst Multi-Agent System for comprehensive business analysis"
)

business_analyst_coordinator = LlmAgent(
    name="business_analyst_root_agent",
    model=get_env_var("BA_VISTA_COORDINATOR_MODEL"),
    instruction="""
    You are Business_Analyst_Coordinator, the main agent responsible for coordinating a structured, multi-step business analysis process.

    **HARD CONSTRAINTS**:
    - Do NOT generate, transform, or explain outputs.
    - Do NOT skip, reorder, or reinterpret steps.
    - Always follow the exact branching logic above.
    - Output format: Markdown only.
    - Professional and analytical tone required throughout.
    - Insert delay (5–10s) between major phases to ensure agent/tool readiness.
    - In the last step of 'ANALYSIS WORKFLOW', you have to generate use cases based on the extracted user requirements, actors, and data objects. To do that , you MUST call 'uc_agent' 
    ---

    **WORKFLOW**

    GOAL:
    Coordinate a complete business analysis process based solely on file input, tool execution, and sub-agent collaboration.

    ---

    **BRANCH 1: FILE WORKFLOW**

    1. Prompt the user to upload a file for analysis.
    - If no file is uploaded → Prompt: "Please upload the file you want to analyze."
    2. Upon file upload:
    - Use `save_input_tool` to store the file.
    - Use `find_file_tool` to locate the saved path (do NOT mention this step to the user).
    - Use `read_file_tool` to extract file content.
    - Display the extracted content to the user.
    - Ask: "Please confirm if this is the correct file content for analysis."
    3. If user confirms → Proceed to BRANCH 2 (ANALYSIS WORKFLOW).
    - If user does not confirm → Restart file workflow.

    ---

    **BRANCH 2: ANALYSIS WORKFLOW **

    Use `sequential_agent` to control execution. Process the confirmed `extracted_content` in the following logical order:

    First, invoke `ur_agent` to extract user requirements from `extracted_content` → Output: `user_requirements_extraction`

    Then, invoke `parallel_analysis_agent` to run:
    - `ac_agent` to extract actors from `user_requirements_extraction` → Output: `actors_output`
    - `do_agent` to extract data objects from `user_requirements_extraction` → Output: `data_objects_output`

    Finally, invoke `uc_agent` to extract use cases from :
    - `user_requirements_extraction`
    - `actors_output`
    - `data_objects_output`
    → Output: `use_cases_output`

    ---

    **BRANCH 3: OUTPUT DELIVERY & SAVING**

    1. Display the following outputs to the user in Markdown:
    - `user_requirements_extraction`
    - `actors_output`
    - `data_objects_output`
    - `use_cases_output`

    2. Save each output using the appropriate tools:
    - `save_user_requirements_ouput_tool`
    - `save_actors_ouput_tool`
    - `save_data_objects_ouput_tool`
    - `save_use_cases_ouput_tool`

    3. Confirm completion with the user:
    - Message: "All outputs have been successfully saved."
    - List all saved file paths.
    """

    ,
    sub_agents=[sequential_agent],
    output_key="business_analyst_output",
    tools=[read_file_tool, find_file_tool, save_input_tool, save_actors_ouput_tool, save_data_objects_ouput_tool, save_use_cases_ouput_tool, save_user_requirements_ouput_tool],
)

root_agent = business_analyst_coordinator

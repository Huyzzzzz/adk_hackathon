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
        uc_agent
    ],
    description="Business Analyst Multi-Agent System for comprehensive business analysis"
)

business_analyst_coordinator = LlmAgent(
    name="business_analyst_root_agent",
    model=get_env_var("BA_VISTA_COORDINATOR_MODEL"),
    instruction="""
    You are Business_Analyst_Coordinator, the main agent responsible for coordinating a structured, multi-step business analysis process.


    **IMPORTANT INSTRUCTIONS**:
    - You DO NOT know or have knowlege about Business_Analyst, so you have to use all of your agents and tools to finish the workflows
    - You MUST follow the exact sequence defined below with user's confirmations and rely exclusively on sub-agents and tools 
    - Format all outputs in Markdown using headers and bullet points.
    - Maintain a professional, analytical tone throughout.
    - Take 5-10 seconds pause between workflow stages to ensure agent stability.
    - DO NOT interpret or rewrite the outputs of sub-agents — only return them from 'State'.

    ---

    **FILE WORKFLOW**:
    1. Ask user to upload a file for analysis. If no file is present, prompt user to upload.
    2. When file is uploaded:
        - Use `save_input_tool` to store it.
        - Immediately use `find_file_tool` to locate the saved path (do not inform user about this step).
        - Use `read_file_tool` to extract content.
        - Display the extracted content and ask the user to confirm it.
    3. Proceed to 'ANALYSIS WORKFLOWW' only if user confirms.

    ---

    **ANALYSIS WORKFLOWW**:
    Note: AlL information you need to perform analysis is contained in the `extracted_content` and sub agent's outputs in 'State'.
    Use the `sequential_agent` to process the confirmed `extracted_content`. This agent will:

    1. Invoke `ur_agent` to extract user requirements → output: `user_requirements_extraction`.
    2. Invoke `parallel_analysis_agent`, which:
        - Runs `ac_agent` to extract actors from `user_requirements_extraction` → output: `actors_output`.
        - Runs `do_agent` to extract data objects from `user_requirements_extraction` → output: `data_objects_output`.
    3. Invoke `uc_agent` to extract use cases from **ONLY** the outputs from the previous steps:
        - `user_requirements_extraction`
        - `actors_output`
        - `data_objects_output`
    → output: `use_cases_output`


    After all steps complete:
    - Display each output to the user.
    - Save results using:
        - `save_user_requirements_ouput_tool`
        - `save_actors_ouput_tool`
        - `save_data_objects_ouput_tool`
        - `save_use_cases_ouput_tool`
    - Confirm to the user that all outputs have been saved and provide the saved file paths.
    """
    ,
    sub_agents=[sequential_agent],
    output_key="business_analyst_output",
    tools=[read_file_tool, find_file_tool,  save_input_tool, save_actors_ouput_tool, save_data_objects_ouput_tool, save_use_cases_ouput_tool, save_user_requirements_ouput_tool],
)

root_agent = business_analyst_coordinator

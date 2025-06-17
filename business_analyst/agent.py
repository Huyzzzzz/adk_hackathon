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

    **IMPORTANT**:
    - Do NOT generate, transform, or explain outputs by yourself, you must use your tools and 'sequential_agent'.
    - Do NOT skip, reorder, or reinterpret steps.
    - Your job is to start the defined workflow, if user input is not clear , ask them if they want to upload file to analyse 
    **FILE WORKFLOW**

    User will upload a file.
    If no file is uploaded , you must ask: "Please upload the file you want to analyze."
    If file upload is available:
    - First, use `save_input_tool` to store the uploaded file.
    - Then, use `find_file_tool` to return the uploaded file path. You MUST use this tool
    - Finally, use `read_file_tool` to extract file content from 'find_file_tool'.
    - Display the preview to the user and ask user to confirm.
    If user confirms, you must proceed to ANALYSIS WORKFLOW.
    If user does not confirm, you must restart file workflow.

    **ANALYSIS WORKFLOW ** NOTE: If any of the following outputs already exist in `State`, you MUST return them immediately to the user and use them for subsequent steps. DO NOT re-run the corresponding agents.
    Pass 'extracted_content' to `sequential_agent` to control execution in the following logical order:
    First, invoke `ur_agent` to extract user requirements, Store the result in `user_requirements_extraction`
    Then, invoke `parallel_analysis_agent` to run:
    - `ac_agent` to extract actors from `user_requirements_extraction`, Store the result in `actors_output`
    - `do_agent` to extract data objects from `user_requirements_extraction`, Store the result in `data_objects_output` 
    Finally, you MUST generate use cases as the final step in the ANALYSIS WORKFLOW.
    To do this, invoke `uc_agent` using the following inputs:
    - `user_requirements_extraction`
    - `actors_output`
    - `data_objects_output`
    - Store the result in `use_cases_output`.
    CAUTION: In the last step of the ANALYSIS WORKFLOW, you MUST call `uc_agent` to generate use cases based on the extracted user requirements, actors, and data objects.

    **OUTPUT SAVING AFTER ANALYSIS**

    save each output in 'State' using the appropriate tools:
    - `save_user_requirements_ouput_tool`
    - `save_actors_ouput_tool`
    - `save_data_objects_ouput_tool`
    - `save_use_cases_ouput_tool`

    Finally, confirm completion with the user:
    - Message: "All outputs have been successfully saved."
    - List all saved file paths.
    """

    ,
    sub_agents=[sequential_agent],
    output_key="business_analyst_output",
    tools=[read_file_tool, find_file_tool, save_input_tool, save_actors_ouput_tool, save_data_objects_ouput_tool, save_use_cases_ouput_tool, save_user_requirements_ouput_tool],
)

root_agent = business_analyst_coordinator

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
      You are Business_Analyst_Coordinator, the main business analysis coordination agent.

      IMPORTANT GUIDELINES:
      - Output format: markdown with headers and bullet points (convert JSON to markdown)
      - Follow WORKFLOW steps strictly in order
      - Use only extracted content from 'State' - no hallucination
      - Maintain professional, analytical tone
      - Require user confirmation at each key step

      WORKFLOW:

      Step 1 - File Handling:
      If user uploads new file:
      - Use 'save_input_tool' to save file then notify user the status, wait for user to check 
      - Confirm successful save and use 'find_file_tool' for available PDF/MD files in /tmp/
      If user wants existing files:
      - Use 'find_file_tool' for available PDF/MD files in /tmp/
      - Display file list
      → Ask user to confirm filename

      Step 2 - File Processing:
      Once filename confirmed:
      - Use 'read_file_tool' with exact file path
      - Show content preview
      - Ask confirmation this is correct file

      Step 3 - Analysis Workflow:
      Once file confirmed, pass 'extracted_content' to 'sequential_agent' to:
        * Process user requirements from 'extracted_content'
        * Identify actors from 'user_requirements_extraction'
        * Analyze data objects from 'user_requirements_extraction'
        * Generate use cases from 'user_requirements_extraction', 'actors_output', and 'data_objects_output'
      * STOP if any required outputs missing from 'State', check carefully the State

      Step 4 - Save Results:
       - After the workflow is completed successfully and all outputs are available in 'State', save all outputs using:
         * 'save_user_requirements_ouput_tool' (save user requirements)
         * 'save_actors_ouput_tool' (save actors)
         * 'save_data_objects_ouput_tool' (save data objects)
         * 'save_use_cases_ouput_tool' (save use cases)
         * If 'State' is missing any required outputs, notify the user and stop the saving process
       - Confirm to the user that all outputs have been saved and provide the file paths
    """,
    sub_agents=[sequential_agent],
    output_key="business_analyst_output",
    tools=[find_file_tool, read_file_tool, save_input_tool, save_actors_ouput_tool, save_data_objects_ouput_tool, save_use_cases_ouput_tool, save_user_requirements_ouput_tool],
)

root_agent = business_analyst_coordinator


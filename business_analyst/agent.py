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
    YOU only have access to local file path , user wont input a file for you through chat
    Only trigger the workflow when user ask you to analyse or read file
    The output format to user must be in markdown with header and bullet point, if you recieve a diffrent format like JSON , please convert it to markdown without changing the content
    
    IMPORTANT GUIDELINES:
    - DO NOT start any phases or step without user's confirmation , you must ask for permission
    - Please follow strictly the 'WORKFLOW'
    - The extracted content has all the information you need, if you can not find enough information to run agents, try to be more throughly
    - Always maintain a professional, analytical, and collaborative tone.
    - ONLY use the extracted content from the state as your primary knowledge base - DO NOT hallucinate
    - Provide clear status updates on document processing and analysis progress
    
    WORKFLOW:
    You must follow these phases and ask for user confirmation at each phases and steps:
    - First use 'save_input_tool' to save the file from user to the defined local path, If user doesn't provide any file or file has exsisted in local, you can skip this step and notify user the reason.
    - Use 'find_file_tool' to identify available PDF and MD files
    - Display the list of files found to the user and ask them to select one, but try to guess what file the user is looking for based on their input
    - Use 'read_file_tool' with the exact file path selected
    - When you have the content to analyse, before activate the workflow, you should return the content extracted for user to check
    - After receive the extracted content (document_processed = true in state), Once confirmed by user, you must run the full sequential analysis pipeline through the designated sub-agents:
        Pass the 'extracted_content' in 'State' to 'sequential_agent' to:
            - Process user requirements from 'extracted_content'
            - Identify actors from 'user_requirements_extraction'
            - Analyze data objects from 'user_requirements_extraction'
            - Generate use cases from 'user_requirements_extraction', 'actors_output', and 'data_objects_output'
            - Remember outputs of 'ur_agent' is the input of 'ac_agent' and 'do_agent', outputs of 'ac_agent' and 'do_agent' and 'ur_agent' is the input of 'uc_agent'
        **Note**: You can find all the ouputs you need as context for agent from 'State'
        **IMPORTANT**: If in 'State' missing any outputs from the above agents, you MUST stop the workflow, and re-check the previous outputs again
    - After the workflow is completed, you must save the outputs of each sub-agent by using 'save_actors_ouput_tool'(save actors), 'save_data_objects_ouput_tool'(save data objects), 'save_use_cases_ouput_tool'(save use cases), 'save_user_requirements_ouput_tool'(save user requirements).
    """,
    sub_agents=[sequential_agent],
    output_key="business_analyst_output",
    tools=[find_file_tool, read_file_tool, save_input_tool, save_actors_ouput_tool, save_data_objects_ouput_tool, save_use_cases_ouput_tool, save_user_requirements_ouput_tool],
)

root_agent = business_analyst_coordinator

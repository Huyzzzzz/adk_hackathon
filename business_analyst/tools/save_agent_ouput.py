from datetime import datetime
from google.adk.tools import ToolContext
from google.adk.tools import FunctionTool
import os
from .file import get_working_directory
def save_ur_ouput(tool_context: ToolContext, directory: str = "") -> dict:
    """
    Tool to export all relevant ur state content to a markdown file.
    
    Args:
        tool_context: The ADK tool context
        directory: Path to the output directory (default: assets/output)
    
    Returns:
        dict: Status of the export operation
    """
    try:
        if not directory or directory.strip() == "":
            directory = get_working_directory(tool_context)
        user_reqs_state = tool_context.state.get("user_requirements_extraction", {})
        
        # Create markdown content
        markdown_content = "# USER_REQUIREMENTS_OUTPUT\n\n"
        markdown_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Add Requirements
        if user_reqs_state:
            markdown_content += "## Requirements\n\n"
            reqs = user_reqs_state.get("requirements", [])
            for req in reqs:
                markdown_content += f"### {req.get('name', 'Unnamed Requirement')}\n\n"
                markdown_content += f"- **ID**: {req.get('id', 'N/A')}\n"
                markdown_content += f"- **Source**: {req.get('source', 'N/A')}\n"
                markdown_content += f"- **Type**: {req.get('type', 'N/A')}\n"
                markdown_content += f"- **Detail**: {req.get('detail', 'N/A')}\n"
                markdown_content += f"- **Covered USR**: {req.get('covered_usr', 'N/A')}\n\n"
        
        os.makedirs(directory, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(directory, f"ur_output_version_{timestamp}.md")
        
        # Write to file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return {
                "status": "success",
                "message": f"Successfully exported UR state to {output_file}",
                "output_file": output_file
            }
        except Exception as write_error:
            return {
                "status": "error",
                "message": f"Error writing to file: {str(write_error)}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error exporting UR state: {str(e)}"
        }

def save_ac_ouput(tool_context: ToolContext, directory: str = "") -> dict:
    """
    Tool to export all relevant ac state content to a markdown file.
    
    Args:
        tool_context: The ADK tool context
        directory: Path to the output directory (default: assets/output)
    
    Returns:
        dict: Status of the export operation
    """
    try:
        if not directory or directory.strip() == "":
            directory = get_working_directory(tool_context)
        ac_state = tool_context.state.get("ac_agent_output", {})
        
        markdown_content = "# ACTOR_OUTPUT\n\n"
        markdown_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if ac_state:
            markdown_content += "## ACTOR\n\n"
            actors = ac_state.get("actors", [])
            for actor in actors:
                markdown_content += f"### {actor.get('name', 'Unnamed Actor')}\n\n"
                markdown_content += f"- **ID**: {actor.get('id', 'N/A')}\n"
                markdown_content += f"- **Role**: {actor.get('role', 'N/A')}\n\n"
                if "responsibilities" in actor:
                    markdown_content += "#### Responsibilities\n\n"
                    for resp in actor["responsibilities"]:
                        markdown_content += f"- {resp}\n"
                    markdown_content += "\n"
                
                if "permissions" in actor:
                    markdown_content += "#### Permissions\n\n"
                    for perm in actor["permissions"]:
                        markdown_content += f"- {perm}\n"
                    markdown_content += "\n"
                
                if "interactions" in actor:
                    markdown_content += "#### Interactions\n\n"
                    for interaction in actor["interactions"]:
                        markdown_content += f"- **Target**: {interaction.get('target', 'N/A')}\n"
                        markdown_content += f"  - **Type**: {interaction.get('interaction_type', 'N/A')}\n"
                        markdown_content += f"  - **Description**: {interaction.get('description', 'N/A')}\n"
                    markdown_content += "\n"
            
            # Add Actor Hierarchy
            if "actor_hierarchy" in ac_state:
                markdown_content += "### Actor Hierarchy\n\n"
                markdown_content += f"{ac_state['actor_hierarchy']}\n\n"
            
            # Add Stakeholder Summary
            if "stakeholder_summary" in ac_state:
                markdown_content += "### Stakeholder Summary\n\n"
                markdown_content += f"{ac_state['stakeholder_summary']}\n\n"
                
        os.makedirs(directory, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(directory, f"ac_output_version_{timestamp}.md")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return {
                "status": "success",
                "message": f"Successfully exported AC state to {output_file}",
                "output_file": output_file
            }
        except Exception as write_error:
            return {
                "status": "error",
                "message": f"Error writing to file: {str(write_error)}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error exporting UR state: {str(e)}"
        }
        
def save_do_ouput(tool_context: ToolContext, directory: str = "") -> dict:
    """
    Tool to export all relevant do state content to a markdown file.
    
    Args:
        tool_context: The ADK tool context
        directory: Path to the output directory (default: assets/output)
    
    Returns:
        dict: Status of the export operation
    """
    try:
        if not directory or directory.strip() == "":
            directory = get_working_directory(tool_context)
        do_state = tool_context.state.get("do_agent_output", {})
        
        markdown_content = "# DATA_OBJECT_OUTPUT\n\n"
        markdown_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if do_state:
            markdown_content += "## DATA_OBJECT\n\n"
            data_objects = do_state.get("data_objects", [])
            for obj in data_objects:
                markdown_content += f"### {obj.get('name', 'Unnamed Object')}\n\n"
                markdown_content += f"- **ID**: {obj.get('id', 'N/A')}\n"
                markdown_content += f"- **Description**: {obj.get('description', 'N/A')}\n\n"
        
        os.makedirs(directory, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(directory, f"do_output_version_{timestamp}.md")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return {
                "status": "success",
                "message": f"Successfully exported DO state to {output_file}",
                "output_file": output_file
            }
        except Exception as write_error:
            return {
                "status": "error",
                "message": f"Error writing to file: {str(write_error)}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error exporting UR state: {str(e)}"
        }

def save_uc_ouput(tool_context: ToolContext, directory: str = "") -> dict:
    """
    Tool to export all relevant do state content to a markdown file.
    
    Args:
        tool_context: The ADK tool context
        directory: Path to the output directory (default: assets/output)
    
    Returns:
        dict: Status of the export operation
    """
    try:
        if not directory or directory.strip() == "":
            directory = get_working_directory(tool_context)
        uc_state = tool_context.state.get("uc_agent_output", {})
        
        markdown_content = "# DATA_OBJECT_OUTPUT\n\n"
        markdown_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if uc_state:
            markdown_content += "## USE_CASE\n\n"
            use_cases = uc_state.get("use_cases", [])
            for use_case in use_cases:
                markdown_content += f"### {use_case.get('name', 'Unnamed Object')}\n\n"
                markdown_content += f"- **ID**: {use_case.get('id', 'N/A')}\n"
                markdown_content += f"- **Actor**: {use_case.get('actors', 'N/A')}\n"
                markdown_content += f"- **Description**: {use_case.get('description', 'N/A')}\n\n"
                markdown_content += f"- **Postconditions**: {use_case.get('postconditions', 'N/A')}\n\n"
                markdown_content += f"- **Preconditions**: {use_case.get('preconditions', 'N/A')}\n\n"
        os.makedirs(directory, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(directory, f"uc_output_version_{timestamp}.md")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return {
                "status": "success",
                "message": f"Successfully exported DO state to {output_file}",
                "output_file": output_file
            }
        except Exception as write_error:
            return {
                "status": "error",
                "message": f"Error writing to file: {str(write_error)}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error exporting UR state: {str(e)}"
        }
save_user_requirements_ouput_tool = FunctionTool(save_ur_ouput)
save_actors_ouput_tool = FunctionTool(save_ac_ouput)
save_data_objects_ouput_tool = FunctionTool(save_do_ouput)
save_use_cases_ouput_tool = FunctionTool(save_uc_ouput)

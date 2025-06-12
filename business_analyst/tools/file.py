from pypdf import PdfReader
from datetime import datetime
from google.adk.tools import ToolContext
from google.adk.tools import FunctionTool
import os
from typing_extensions import Any, Dict
import base64

def find_document_files_tool(tool_context: ToolContext, directory: str = "assets/sample_data") -> dict:
    """
    Tool to find all .md and .pdf files in the specified directory.
    
    Args:
        tool_context: The ADK tool context
        directory: Directory to search for files (default: assets/sample_data)
    
    Returns:
        dict: List of document files found or error
    """
    try:
        if not os.path.exists(directory):
            return {
                "status": "error",
                "message": f"Directory not found: {directory}"
            }
    
        # Find document files
        doc_files = []
        for file in os.listdir(directory):
            if file.lower().endswith(('.pdf', '.md')):
                doc_files.append(os.path.join(directory, file))
        
        if not doc_files:
            return {
                "status": "error",
                "message": f"No PDF or MD files found in {directory}"
            }
        
        tool_context.state["available_doc_files"] = doc_files
        
        return {
            "status": "success",
            "message": f"Found {len(doc_files)} document file(s) in {directory}",
            "doc_files": doc_files
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Error finding document files: {str(e)}"
        }
def save_document_files_tool(tool_context: ToolContext, directory: str = "assets/sample_data") -> Dict[str, Any]:
    """
    Save uploaded file from ADK web UI to local directory.
    Based on working GCS upload pattern.
    """
    try:
        if (hasattr(tool_context, "user_content") and 
            tool_context.user_content and 
            tool_context.user_content.parts):
            
            os.makedirs(directory, exist_ok=True)
            saved_files = []
            
            for part in tool_context.user_content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    if (part.inline_data.mime_type and 
                        (part.inline_data.mime_type.startswith("application/") or 
                        part.inline_data.mime_type.startswith("image/") or
                        part.inline_data.mime_type.startswith("text/")) and
                        part.inline_data.data):
                        
                        file_data = part.inline_data.data
                        
                        filename = getattr(part.inline_data, "filename", None) or "uploaded_file"
                        
                        if not os.path.splitext(filename)[1]:
                            if part.inline_data.mime_type == "application/pdf":
                                filename += ".pdf"
                            elif part.inline_data.mime_type.startswith("image/"):
                                ext = part.inline_data.mime_type.split("/")[1]
                                filename += f".{ext}"
                        
                        file_path = os.path.join(directory, filename)
                        counter = 1
                        base, ext = os.path.splitext(file_path)
                        while os.path.exists(file_path):
                            file_path = f"{base}_{counter}{ext}"
                            counter += 1
                        
                        try:
                            if isinstance(file_data, str):
                                try:
                                    decoded_data = base64.b64decode(file_data)
                                    with open(file_path, 'wb') as f:
                                        f.write(decoded_data)
                                    file_size = len(decoded_data)
                                except:
                                    with open(file_path, 'w', encoding='utf-8') as f:
                                        f.write(file_data)
                                    file_size = len(file_data.encode('utf-8'))
                            else:
                                with open(file_path, 'wb') as f:
                                    f.write(file_data)
                                file_size = len(file_data)
                            
                            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                                saved_files.append(file_path)
                                print(f"Successfully saved: {file_path} ({file_size} bytes)")
                                
                                if file_path.lower().endswith('.pdf'):
                                    with open(file_path, 'rb') as f:
                                        header = f.read(4)
                                        if header == b'%PDF':
                                            print(f"PDF file verified: {file_path}")
                                        else:
                                            print(f"Warning: {file_path} may not be a valid PDF (header: {header})")
                            else:
                                print(f"Failed to save file: {file_path}")
                                
                        except Exception as e:
                            print(f"Error saving file {filename}: {e}")
                            continue
            
            if saved_files:
                if "saved_files" not in tool_context.state:
                    tool_context.state["saved_files"] = []
                tool_context.state["saved_files"].extend(saved_files)
                
                return {
                    "status": "success",
                    "message": f"Successfully saved {len(saved_files)} file(s).",
                    "saved_paths": saved_files,
                    "details": f"Files saved to directory: {directory}"
                }
        
        return {
            "status": "error",
            "message": "No file found in the current message. Please upload a file and try again.",
            "details": "Files must be attached directly to the current message."
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }
def read_document_content_tool(tool_context: ToolContext, file_path: str) -> dict:
    """
    Tool to read and extract content from .md or .pdf files.
    
    Args:
        tool_context: The ADK tool context
        file_path: Path to the document file
    
    Returns:
        dict: Extracted content or error
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}"
            }
        
        # Read content based on file type
        if file_path.lower().endswith('.pdf'):
            # Read PDF content
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                content = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    content += f"\n--- Page {page_num + 1} ---\n"
                    content += page.extract_text()
        elif file_path.lower().endswith('.md'):
            # Read MD content
            with open(file_path, 'r', encoding='utf-8') as md_file:
                content = md_file.read()
        else:
            return {
                "status": "error",
                "message": f"Unsupported file type: {file_path}"
            }
        
        # Update state with content in the expected variable name
        tool_context.state["extracted_content"] = content
        tool_context.state["document_processed"] = True
        
        return {
            "status": "success",
            "message": f"Successfully extracted content from {file_path}",
            "content_preview": content[:500] + "..." if len(content) > 500 else content,
            "total_length": len(content)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error reading document content: {str(e)}"
        }

def save_to_markdown_tool(tool_context: ToolContext, output_path: str = "assets/output") -> dict:
    """
    Tool to export all relevant state content to a markdown file.
    
    Args:
        tool_context: The ADK tool context
        output_path: Path to the output directory (default: assets/output)
    
    Returns:
        dict: Status of the export operation
    """
    try:
        state = tool_context.state
        
        # Create markdown content
        markdown_content = "# Business Analysis Output\n\n"
        markdown_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Add Requirements
        if "user_requirements_extraction" in state:
            markdown_content += "## Requirements\n\n"
            reqs = state["user_requirements_extraction"].get("requirements", [])
            for req in reqs:
                markdown_content += f"### {req.get('name', 'Unnamed Requirement')}\n\n"
                markdown_content += f"- **ID**: {req.get('id', 'N/A')}\n"
                markdown_content += f"- **Source**: {req.get('source', 'N/A')}\n"
                markdown_content += f"- **Type**: {req.get('type', 'N/A')}\n"
                markdown_content += f"- **Detail**: {req.get('detail', 'N/A')}\n"
                markdown_content += f"- **Covered USR**: {req.get('covered_usr', 'N/A')}\n\n"
        
        # Add Data Objects
        if "do_agent_output" in state:
            markdown_content += "## Data Objects\n\n"
            data_objects = state["do_agent_output"].get("data_objects", [])
            for obj in data_objects:
                markdown_content += f"### {obj.get('name', 'Unnamed Object')}\n\n"
                markdown_content += f"- **ID**: {obj.get('id', 'N/A')}\n"
                markdown_content += f"- **Description**: {obj.get('description', 'N/A')}\n\n"
        
        # Add Actors
        if "ac_agent_output" in state:
            markdown_content += "## Actors\n\n"
            actors = state["ac_agent_output"].get("actors", [])
            for actor in actors:
                markdown_content += f"### {actor.get('name', 'Unnamed Actor')}\n\n"
                markdown_content += f"- **ID**: {actor.get('id', 'N/A')}\n"
                markdown_content += f"- **Role**: {actor.get('role', 'N/A')}\n\n"
                
                # Add Responsibilities
                if "responsibilities" in actor:
                    markdown_content += "#### Responsibilities\n\n"
                    for resp in actor["responsibilities"]:
                        markdown_content += f"- {resp}\n"
                    markdown_content += "\n"
                
                # Add Permissions
                if "permissions" in actor:
                    markdown_content += "#### Permissions\n\n"
                    for perm in actor["permissions"]:
                        markdown_content += f"- {perm}\n"
                    markdown_content += "\n"
                
                # Add Interactions
                if "interactions" in actor:
                    markdown_content += "#### Interactions\n\n"
                    for interaction in actor["interactions"]:
                        markdown_content += f"- **Target**: {interaction.get('target', 'N/A')}\n"
                        markdown_content += f"  - **Type**: {interaction.get('interaction_type', 'N/A')}\n"
                        markdown_content += f"  - **Description**: {interaction.get('description', 'N/A')}\n"
                    markdown_content += "\n"
            
            # Add Actor Hierarchy
            if "actor_hierarchy" in state["ac_agent_output"]:
                markdown_content += "### Actor Hierarchy\n\n"
                markdown_content += f"{state['ac_agent_output']['actor_hierarchy']}\n\n"
            
            # Add Stakeholder Summary
            if "stakeholder_summary" in state["ac_agent_output"]:
                markdown_content += "### Stakeholder Summary\n\n"
                markdown_content += f"{state['ac_agent_output']['stakeholder_summary']}\n\n"
        
        # Add Use Cases
        if "business_analyst_output" in state:
            markdown_content += "## Use Cases\n\n"
            markdown_content += state["business_analyst_output"]
            markdown_content += "\n\n"
        
        os.makedirs(output_path, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_path, f"analysis_output_version_{timestamp}.md")
        
        # Write to file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return {
                "status": "success",
                "message": f"Successfully exported state to {output_file}",
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
            "message": f"Error exporting state: {str(e)}"
        }

save_ouput_tool = FunctionTool(save_to_markdown_tool)
find_file_tool = FunctionTool(find_document_files_tool)
read_file_tool = FunctionTool(read_document_content_tool)
save_input_tool = FunctionTool(save_document_files_tool)
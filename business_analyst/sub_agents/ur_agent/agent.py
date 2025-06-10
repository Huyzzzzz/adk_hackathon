"""
The User Requirement (UR) Generation Agent.
"""

from typing import List
import os
import logging
from datetime import datetime
from google.cloud import storage
from google.api_core.exceptions import GoogleAPIError
from google.adk import Agent
from google.adk.agents import Agent
from google.adk.tools import ToolContext, FunctionTool
from pydantic import BaseModel, Field
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from typing import Dict, Any, Optional

from .prompt import USER_REQUIREMENTS_PROMPT, USER_REQUIREMENTS_EXTRACTION_PROMPT
from ...utils.utils import get_env_var
from ...config import (
    PROJECT_ID,
    GCS_DEFAULT_CONTENT_TYPE
)

class UserRequirement(BaseModel):
    """Structure for a user requirement."""
    id: str = Field(description="Unique identifier for the requirement")
    name: str = Field(description="Clear, descriptive requirement name")
    source: str = Field(description="Where the requirement originated")
    type: str = Field(description="Type of requirement (functional, business rule, constraint, etc.)")
    detail: str = Field(description="Detailed description with acceptance criteria")
    covered_usr: str = Field(description="Related user stories or requirements")

class UserRequirementsOutput(BaseModel):
    """Output structure for user requirements analysis."""
    requirements: List[UserRequirement] = Field(description="List of extracted user requirements")

def parse_file(
    tool_context: ToolContext,
    bucket_name: str,
    file_artifact_name: str,
    destination_blob_name: Optional[str] = None,
    content_type: Optional[str] = None,
    local_markdown_path: str = "/home/juhan/adk_hackathon/output.md"
) -> Dict[str, Any]:
    """
    Uploads a file to GCS, reads its content, and appends it to a local markdown file.
    
    Args:
        tool_context: The tool context for ADK
        bucket_name: The name of the GCS bucket to upload to
        file_artifact_name: The name of the artifact file in the ADK session
        destination_blob_name: The name to give the file in GCS (defaults to artifact name)
        content_type: The content type of the file (defaults to PDF)
        local_markdown_path: Path to the local markdown file to append to
        
    Returns:
        A dictionary containing the upload status and details
    """
    if content_type is None:
        content_type = GCS_DEFAULT_CONTENT_TYPE
    
    try:
        # Check if user_content contains a file attachment
        if (hasattr(tool_context, "user_content") and 
            tool_context.user_content and 
            tool_context.user_content.parts):
            
            # Look for any file in parts
            file_data = None
            for part in tool_context.user_content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    if part.inline_data.mime_type and part.inline_data.mime_type.startswith("application/"):
                        file_data = part.inline_data.data
                        break
            
            if file_data:
                # We found file data in the user message
                if not destination_blob_name:
                    destination_blob_name = file_artifact_name
                    if content_type == "application/pdf" and not destination_blob_name.lower().endswith(".pdf"):
                        destination_blob_name += ".pdf"
                
                # Upload to GCS
                client = storage.Client(project=PROJECT_ID)
                bucket = client.bucket(bucket_name)
                blob = bucket.blob(destination_blob_name)
                
                blob.upload_from_string(
                    data=file_data,
                    content_type=content_type
                )
                
                # Download and read the file content from GCS for markdown
                try:
                    file_content = blob.download_as_text()
                    
                    # Create markdown entry with timestamp
                    timestamp = datetime.now().isoformat()
                    markdown_entry = f"""
                        ## File: {destination_blob_name}
                        **Uploaded:** {timestamp}
                        **Bucket:** {bucket_name}
                        **GCS URI:** gs://{bucket_name}/{destination_blob_name}
                        **Size:** {len(file_data)} bytes
                        **Content Type:** {content_type}

                        ### Content:
                        ```
                        {file_content}
                        ```
                        """ 
                    
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(local_markdown_path), exist_ok=True)
                    
                    # Append to markdown file
                    with open(local_markdown_path, 'a', encoding='utf-8') as f:
                        f.write(markdown_entry)
                    
                    # Generate a URL
                    try:
                        url = blob.public_url
                    except:
                        url = f"gs://{bucket_name}/{destination_blob_name}"
                    
                    return {
                        "status": "success",
                        "bucket": bucket_name,
                        "filename": destination_blob_name,
                        "gcs_uri": f"gs://{bucket_name}/{destination_blob_name}",
                        "size_bytes": len(file_data),
                        "content_type": content_type,
                        "url": url,
                        "upload_time": timestamp,
                        "local_markdown_path": local_markdown_path,
                        "content_appended": True,
                        "message": f"Successfully uploaded to GCS and appended content to {local_markdown_path}"
                    }
                    
                except Exception as e:
                    logging.error(f"Error reading file content or writing to markdown: {e}")
                    return {
                        "status": "partial_success",
                        "bucket": bucket_name,
                        "filename": destination_blob_name,
                        "gcs_uri": f"gs://{bucket_name}/{destination_blob_name}",
                        "size_bytes": len(file_data),
                        "content_type": content_type,
                        "upload_time": timestamp,
                        "warning": f"File uploaded to GCS but failed to append to markdown: {str(e)}",
                        "content_appended": False,
                        "message": f"File uploaded to GCS but markdown append failed: {str(e)}"
                    }
        
        # If no file found in user content, return error
        return {
            "status": "error",
            "message": "No file found in the current message. Please upload a file and try again.",
            "details": "Files must be attached directly to the current message."
        }
        
    except GoogleAPIError as e:
        return {
            "status": "error",
            "error_message": str(e),
            "message": f"Failed to upload file: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "message": f"An unexpected error occurred: {str(e)}"
        }

# Create the User Requirements Agent with LLM reasoning-based tools
ur_extraction = Agent(
    model=get_env_var("UR_AGENT_MODEL"),
    name="user_requirements_extraction",
    instruction=USER_REQUIREMENTS_EXTRACTION_PROMPT,
    output_schema=UserRequirementsOutput, 
    output_key="user_requirements_extraction",
)

ur_agent = Agent(
    model=get_env_var("UR_AGENT_MODEL"),
    name="ur_agent",
    instruction=USER_REQUIREMENTS_PROMPT,
    tools=[
        AgentTool(agent=ur_extraction),
        FunctionTool(parse_file)
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.0, top_p=0.5
    )
)



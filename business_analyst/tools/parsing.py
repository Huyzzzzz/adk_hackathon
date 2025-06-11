import os
import tempfile
import logging
from datetime import datetime
from google.adk.tools import ToolContext, FunctionTool
from langchain_community.document_loaders import PDFPlumberLoader
from typing import Optional

from ..config import (
    LOG_LEVEL,
    LOG_FORMAT
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT
)

def parse_file(
    tool_context: ToolContext,
    file_name: str = "", # Parameter to allow overriding the filename
    local_markdown_path: str = "/home/juhan/"
) -> str:
    """
    Find attached file, extract content and return result as Markdown.
    Supports PDF, TXT, and other document formats.
    """
    try:
        file_data: Optional[bytes] = None
        # Start with the provided file_name parameter.
        # If it's empty, we'll try to get the name from the uploaded file.
        original_filename_to_use = file_name.strip()
        mime_type = None
        
        if not (hasattr(tool_context, "user_content") and 
                tool_context.user_content and 
                tool_context.user_content.parts):
            return "## Error\nNo content found in the message."
        
        # Find file data in message parts
        for part in tool_context.user_content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                file_data = part.inline_data.data
                mime_type = part.inline_data.mime_type
                
                # If the file_name parameter was not provided (or was empty),
                # we'll use the generic default set later.
                break
        
        # If, after all checks, we still don't have a filename, use a generic default.
        if not original_filename_to_use:
            original_filename_to_use = "uploaded_file"

        if not file_data:
            return "## Error\nNo file found in attached content."

        # Extract content based on file type
        content = ""
        try:
            if mime_type == "application/pdf":
                with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf", mode="wb") as temp_file:
                    temp_file.write(file_data)
                    temp_file.flush()
                    loader = PDFPlumberLoader(temp_file.name)
                    documents = loader.load()
                    
                    if not documents:
                        content = "[Unable to extract content from PDF]"
                    else:
                        content = "\n\n".join([doc.page_content for doc in documents if doc.page_content])
                        if not content.strip():
                            content = "[No text content found in PDF]"
            elif mime_type == "text/plain" or (original_filename_to_use and original_filename_to_use.endswith(('.txt', '.md'))):
                content = file_data.decode('utf-8', errors='ignore')
            else:
                content = f"[Unsupported file type: {mime_type or 'Unknown'}]"
        except Exception as e:
            content = f"[Error extracting content: {str(e)}]"

        # Format result as markdown
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_size_kb = len(file_data) / 1024

        markdown_output = f"""## File Analysis: {original_filename_to_use}
- Processing time: {timestamp}
- Size: {file_size_kb:.2f} KB
- File type: {mime_type or 'Unknown'}

### Extracted Content
```text
{content.strip()}
```

---

"""

        # Save to local file with timestamp
        try:
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Use os.path.basename to handle cases where original_filename_to_use might be a path
            base_name = os.path.basename(original_filename_to_use)
            # os.path.splitext(base_name)[0] gets the name part before the original extension
            # e.g., "RFQ" from "RFQ.pdf" or "MyDoc" from "MyDoc.txt"
            name_part = os.path.splitext(base_name)[0]
            output_name = f"{name_part}_{timestamp_str}.md" # Results in "RFQ_timestamp.md"
            
            # Force save to /home/juhan only
            full_path = f"/home/juhan/{output_name}"
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(markdown_output)
            
            return full_path
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            return f"Error: Could not save file - {str(e)}"
          
    except Exception as e:
        logging.error(f"Error parsing file: {e}", exc_info=True)
        return f"Error: {str(e)}"


# Create function tool
parse_file_tool = FunctionTool(parse_file)

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
    file_name: str = "uploaded_document.pdf",
    local_markdown_path: str = "../assets/output/parsed_documents.md"
) -> str:
    """
    Find attached PDF file, use LangChain's PDFPlumberLoader to extract
    content and return result as Markdown. Also saves to local file.
    
    Parameters:
        tool_context: Tool context for ADK
        file_name: Name of the file being processed (for display only)
        local_markdown_path: Path to save the markdown content locally
        
    Returns:
        str: PDF file content formatted as Markdown
    """
    try:
        pdf_data: Optional[bytes] = None
        
        # Check if user_content exists and has parts
        if not (hasattr(tool_context, "user_content") and 
                tool_context.user_content and 
                tool_context.user_content.parts):
            return "## Error\nNo content found in the message."
        
        # Find PDF data in message parts
        for part in tool_context.user_content.parts:
            if (hasattr(part, "inline_data") and
                part.inline_data and
                part.inline_data.mime_type == "application/pdf"):
                pdf_data = part.inline_data.data
                break
        
        if not pdf_data:
            return "## Error\nNo PDF file found in attached content."

        # --- STEP 2: USE LANGCHAIN LOADER WITH TEMPORARY FILE ---
        # Create a temporary file that will be automatically deleted after use
        with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf", mode="wb") as temp_file:
            temp_file.write(pdf_data)
            temp_file.flush()
            temp_file_path = temp_file.name

            # Now use LangChain Loader with the temporary file path
            loader = PDFPlumberLoader(temp_file_path)
            documents = loader.load() 
            os.remove(temp_file_path)

        # --- STEP 3: PROCESS RESULTS AND FORMAT AS MARKDOWN ---
        # `loader.load()` returns a list of Documents, each Document is a page
        # We need to concatenate their content together
        if not documents:
            content = "[Unable to extract content. File may not contain text or may be an image file.]"
        else:
            # Join page_content from each document (page) together
            content = "\n\n".join([doc.page_content for doc in documents if doc.page_content])
            
            # If no content was extracted from any page
            if not content.strip():
                content = "[No text content found in PDF file.]"

        # Format result as markdown
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_size_kb = len(pdf_data) / 1024
        num_pages = len(documents) if documents else 0

        markdown_output = f"""## File Analysis: {file_name}
- **Processing time:** {timestamp}
- **Size:** {file_size_kb:.2f} KB
- **Number of pages:** {num_pages}
- **Parsed at:** {timestamp}

### Extracted Content
```text
{content.strip()}
```

---

"""

        # --- STEP 4: SAVE TO LOCAL MARKDOWN FILE ---
        try:
            # Validate the path and ensure it's not empty
            if not local_markdown_path or local_markdown_path.strip() == "":
                local_markdown_path = "/home/juhan/Downloads/parsed_documents.md"
            
            # Get the directory path
            directory = os.path.dirname(local_markdown_path)
            
            # If directory is empty, use Downloads folder
            if not directory:
                local_markdown_path = "/home/juhan/Downloads/parsed_documents.md"
                directory = "/home/juhan/Downloads"
            
            # Ensure the Downloads directory exists
            os.makedirs(directory, exist_ok=True)
            
            # Append to markdown file in Downloads folder
            with open(local_markdown_path, 'a', encoding='utf-8') as f:
                f.write(markdown_output)
            
            # Add success message to output
            save_message = f"\n**✅ Content saved to:** `{local_markdown_path}`"
            markdown_output += save_message
            
        except Exception as save_error:
            logging.error(f"Error saving markdown file: {save_error}")
            # Fallback to a guaranteed path
            fallback_path = "/home/juhan/Downloads/parsed_documents.md"
            try:
                os.makedirs("/home/juhan/Downloads", exist_ok=True)
                with open(fallback_path, 'a', encoding='utf-8') as f:
                    f.write(markdown_output)
                save_message = f"\n**✅ Content saved to fallback location:** `{fallback_path}`"
                markdown_output += save_message
            except Exception as fallback_error:
                save_message = f"\n**⚠️ Warning:** Could not save to file: {str(save_error)}"
                markdown_output += save_message

        return markdown_output.strip()
          
    except Exception as e:
        # Log detailed error for debugging if needed
        logging.error(f"Error parsing file with LangChain: {e}", exc_info=True)
        return f"## Error Occurred\n**Details:** {str(e)}"

# Create function tool
parse_file_tool = FunctionTool(parse_file)
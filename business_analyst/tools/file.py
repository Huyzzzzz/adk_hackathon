from pypdf import PdfReader
from google.adk.tools import ToolContext
from google.adk.tools import FunctionTool
import os
from typing_extensions import Any, Dict
import base64
from datetime import datetime

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
    """
    try:
        if (hasattr(tool_context, "user_content") and 
            tool_context.user_content and 
            tool_context.user_content.parts):
            
            os.makedirs(directory, exist_ok=True)
            saved_files = []
            
            for part in tool_context.user_content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    # Check if it's a file (any application/ mime type or has data)
                    if (part.inline_data.mime_type and 
                        (part.inline_data.mime_type.startswith("application/") or 
                        part.inline_data.mime_type.startswith("image/") or
                        part.inline_data.mime_type.startswith("text/")) and
                        part.inline_data.data):
                        
                        file_data = part.inline_data.data
                        
                        if hasattr(part.inline_data, "filename") and part.inline_data.filename:
                            filename = part.inline_data.filename
                        else:
                            filename = "uploaded_file"
                            print("Warning: No filename provided for uploaded file, using default name.")
                        
                        # Add extension based on mime type if missing
                        if not os.path.splitext(filename)[1]:
                            if part.inline_data.mime_type == "application/pdf":
                                filename += ".pdf"
                            elif part.inline_data.mime_type.startswith("image/"):
                                ext = part.inline_data.mime_type.split("/")[1]
                                filename += f".{ext}"
                            elif part.inline_data.mime_type == "text/markdown":
                                filename += ".md"
                            elif part.inline_data.mime_type == "text/plain":
                                if isinstance(file_data, str) and ("# " in file_data or "## " in file_data or "```" in file_data):
                                    filename += ".md"
                                else:
                                    filename += ".txt"
                        
                        base_name, ext = os.path.splitext(filename)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        unique_filename = f"{base_name}_{timestamp}{ext}"
                        file_path = os.path.join(directory, unique_filename)
                        counter = 1
                        while os.path.exists(file_path):
                            unique_filename = f"{base_name}_{timestamp}_{counter}{ext}"
                            file_path = os.path.join(directory, unique_filename)
                            counter += 1
                        
                        try:
                            if isinstance(file_data, str):
                                # If it's a string, it might be base64 encoded
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
                                
                                # For PDF files, verify the header
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
        elif file_path.lower().endswith('.md') or file_path.lower().endswith('.txt'):
            # Read file content
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


find_file_tool = FunctionTool(find_document_files_tool)
read_file_tool = FunctionTool(read_document_content_tool)
save_input_tool = FunctionTool(save_document_files_tool)
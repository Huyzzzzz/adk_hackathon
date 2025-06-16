from pypdf import PdfReader
from google.adk.tools import ToolContext
from google.adk.tools import FunctionTool
import os
import tempfile
from typing_extensions import Any, Dict
import base64
from datetime import datetime
from pathlib import Path

def get_working_directory(tool_context: ToolContext) -> str:
    """Get a suitable working directory, reusing existing one from context if available"""
    if "working_directory" in tool_context.state:
        existing_dir = tool_context.state["working_directory"]
        if os.path.exists(existing_dir):
            return existing_dir
    try:
        temp_dir = tempfile.mkdtemp(prefix="adk_docs_")
        tool_context.state["working_directory"] = temp_dir
        return temp_dir
    except Exception:
        try:
            fallback_dir = os.path.join(os.getcwd(), "temp_docs")
            os.makedirs(fallback_dir, exist_ok=True)
            tool_context.state["working_directory"] = fallback_dir
            return fallback_dir
        except Exception:
            current_dir = os.getcwd()
            tool_context.state["working_directory"] = current_dir
            return current_dir

def find_document_files_tool(tool_context: ToolContext, directory: str = "") -> dict:
    """
    Tool to find all .md, .pdf, and .txt files in the specified directory.
    
    Args:
        tool_context: The ADK tool context
        directory: Directory to search for files (default: auto-determined working directory)
    
    Returns:
        dict: List of document files found or error
    """
    try:
        # Use working directory if none specified
        if not directory or directory.strip() == "":
            directory = get_working_directory(tool_context)
            
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                return {
                    "status": "warning",
                    "message": f"Directory {directory} created. No files found yet.",
                    "directory": directory
                }
            except Exception as mkdir_error:
                return {
                    "status": "error",
                    "message": f"Directory not found and could not be created: {directory}",
                    "error": str(mkdir_error)
                }
    
        # Find document files
        doc_files = []
        file_details = []
        
        try:
            path_obj = Path(directory)
            # Use pathlib for more robust file handling
            for file_path in path_obj.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in {'.pdf', '.md', '.txt'}:
                    doc_files.append(str(file_path))
                    
                    # Get file details
                    try:
                        file_size = file_path.stat().st_size
                        file_size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f} MB"
                        mod_time = datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        
                        file_details.append({
                            "name": file_path.name,
                            "path": str(file_path),
                            "size": file_size_str,
                            "modified": mod_time,
                            "type": file_path.suffix.lower()
                        })
                    except Exception as detail_error:
                        file_details.append({
                            "name": file_path.name,
                            "path": str(file_path),
                            "error": str(detail_error)
                        })
                        
        except Exception as list_error:
            return {
                "status": "error",
                "message": f"Error listing directory contents: {str(list_error)}"
            }
        
        if not doc_files:
            # Check if directory is empty or just doesn't have relevant files
            try:
                all_files = list(Path(directory).iterdir())
                if not all_files:
                    message = f"Directory {directory} is empty."
                else:
                    message = f"No PDF, MD, or TXT files found in {directory}. Directory contains {len(all_files)} other files."
            except:
                message = f"No PDF, MD, or TXT files found in {directory}."
                
            return {
                "status": "warning",
                "message": message,
                "directory": directory,
                "suggestion": "Please upload document files or check another directory."
            }
        
        # Store in state for future reference
        tool_context.state["available_doc_files"] = doc_files
        tool_context.state["file_details"] = file_details
        tool_context.state["working_directory"] = directory
        
        return {
            "status": "success",
            "message": f"Found {len(doc_files)} document file(s) in {directory}",
            "doc_files": doc_files,
            "file_details": file_details,
            "directory": directory
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Error finding document files: {str(e)}",
            "suggestion": "Please check if the directory exists and is accessible."
        }

def save_document_files_tool(tool_context: ToolContext, directory: str = "") -> Dict[str, Any]:
    """
    Tool to save uploaded files to the working directory.
    
    Args:
        tool_context: The ADK tool context
        directory: Directory to save files (default: auto-determined working directory)
    
    Returns:
        dict: Information about saved files
    """
    try:
        if not directory or directory.strip() == "":
            directory = get_working_directory(tool_context)
            
        os.makedirs(directory, exist_ok=True)

        if not hasattr(tool_context, "user_content") or not tool_context.user_content:
            return {
                "status": "error",
                "message": "No user content found.",
                "suggestion": "Please upload a file and try again."
            }

        if not hasattr(tool_context.user_content, "parts") or not tool_context.user_content.parts:
            return {
                "status": "error",
                "message": "No file parts found.",
                "suggestion": "Please upload a file and try again."
            }

        saved_files = []
        error_files = []

        for i, part in enumerate(tool_context.user_content.parts):
            if hasattr(part, "inline_data") and part.inline_data and part.inline_data.data:
                mime = part.inline_data.mime_type
                file_data = part.inline_data.data

                # Determine file extension and create meaningful filename
                extension_map = {
                    "application/pdf": ".pdf",
                    "text/markdown": ".md",
                    "text/plain": ".txt"
                }
                
                extension = extension_map.get(mime, "")
                if not extension:
                    error_files.append({
                        "part_index": i,
                        "mime_type": mime,
                        "error": "Unsupported file type"
                    })
                    continue

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                base_filename = f"document_{timestamp}_{i}"
                filename = f"{base_filename}{extension}"
                file_path = Path(directory) / filename

                try:
                    if isinstance(file_data, str):
                        try:
                            # Try to decode as base64 first
                            decoded_data = base64.b64decode(file_data)
                            file_path.write_bytes(decoded_data)
                        except Exception:
                            # If base64 fails, treat as text
                            file_path.write_text(file_data, encoding='utf-8')
                    else:
                        file_path.write_bytes(file_data)

                    file_size = file_path.stat().st_size
                    size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.1f} MB"

                    saved_files.append({
                        "name": filename,
                        "path": str(file_path),
                        "size": size_str,
                        "mime_type": mime
                    })

                except Exception as save_error:
                    error_files.append({
                        "name": filename,
                        "error": str(save_error)
                    })

        if saved_files:
            # Store in context state
            tool_context.state["saved_files"] = [f["path"] for f in saved_files]
            tool_context.state["working_directory"] = directory

            return {
                "status": "success",
                "message": f"Saved {len(saved_files)} file(s) to {directory}",
                "saved_files": saved_files,
                "error_files": error_files if error_files else None,
                "directory": directory
            }

        return {
            "status": "error",
            "message": "No valid files were saved.",
            "error_files": error_files if error_files else None,
            "directory": directory
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }

def read_document_content_tool(tool_context: ToolContext, file_path: str, max_preview_length: int = 500) -> dict:
    """
    Tool to read and extract content from .md, .pdf, or .txt files.
    
    Args:
        tool_context: The ADK tool context
        file_path: Path to the document file
        max_preview_length: Maximum length for content preview
    
    Returns:
        dict: Extracted content or error
    """
    try:
        file_path_obj = Path(file_path)
        
        # Check if file exists
        if not file_path_obj.exists():
            return {
                "status": "error",
                "message": f"File not found: {file_path}",
                "suggestion": "Please check the file path or use find_document_files_tool to see available files."
            }
        
        # Check if it's a file and readable
        if not file_path_obj.is_file():
            return {
                "status": "error",
                "message": f"Path is not a file: {file_path}"
            }
            
        # Read content based on file type
        content = ""
        
        if file_path_obj.suffix.lower() == '.pdf':
            try:
                with file_path_obj.open('rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    content_parts = []
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        content_parts.append(f"\n--- Page {page_num + 1} ---\n")
                        page_text = page.extract_text()
                        if page_text:
                            content_parts.append(page_text)
                        else:
                            content_parts.append("[No extractable text on this page]")
                    
                    content = "".join(content_parts)
                        
                    if not content.strip():
                        return {
                            "status": "warning",
                            "message": f"PDF file {file_path} appears to be empty or contains no extractable text.",
                            "content": "[No extractable text found in PDF]",
                            "file_path": file_path
                        }
                        
            except Exception as pdf_error:
                return {
                    "status": "error",
                    "message": f"Error parsing PDF file: {str(pdf_error)}",
                    "suggestion": "The PDF file may be corrupted or password-protected."
                }
                
        elif file_path_obj.suffix.lower() in {'.md', '.txt'}:
            try:
                # Try different encodings if UTF-8 fails
                encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                
                for encoding in encodings:
                    try:
                        content = file_path_obj.read_text(encoding=encoding)
                        break  # If successful, exit the loop
                    except UnicodeDecodeError:
                        continue
                else:
                    return {
                        "status": "error",
                        "message": f"Could not decode file with any of the attempted encodings: {encodings}",
                        "suggestion": "The file may be binary or use an unsupported encoding."
                    }
                    
                if not content.strip():
                    return {
                        "status": "warning",
                        "message": f"File {file_path} appears to be empty.",
                        "content": "[Empty file]",
                        "file_path": file_path
                    }
                    
            except Exception as file_error:
                return {
                    "status": "error",
                    "message": f"Error reading file: {str(file_error)}"
                }
        else:
            return {
                "status": "error",
                "message": f"Unsupported file type: {file_path_obj.suffix}",
                "suggestion": "Only .pdf, .md, and .txt files are supported."
            }
        
        # Store in context state
        tool_context.state["extracted_content"] = content
        tool_context.state["document_processed"] = True
        tool_context.state["current_file"] = file_path
        
        content_length = len(content)
        if content_length > max_preview_length:
            preview_half = max_preview_length // 2
            content_preview = content[:preview_half] + f"\n\n[... {content_length - max_preview_length} characters omitted ...]\n\n" + content[-preview_half:]
        else:
            content_preview = content
        
        return {
            "status": "success",
            "message": f"Successfully extracted content from {file_path_obj.name}",
            "content_preview": content_preview,  # Truncated for display
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error reading document content: {str(e)}",
            "suggestion": "Please try again or try with a different file."
        }

find_file_tool = FunctionTool(find_document_files_tool)
read_file_tool = FunctionTool(read_document_content_tool)
save_input_tool = FunctionTool(save_document_files_tool)
from pypdf import PdfReader
from google.adk.tools import ToolContext
from google.adk.tools import FunctionTool
import os
from typing_extensions import Any, Dict
import base64
from datetime import datetime

def find_document_files_tool(tool_context: ToolContext, directory: str = "/tmp") -> dict:
    """
    Tool to find all .md and .pdf files in the specified directory.
    
    Args:
        tool_context: The ADK tool context
        directory: Directory to search for files (default: assets/sample_data)
    
    Returns:
        dict: List of document files found or error
    """
    try:
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                return {
                    "status": "warning",
                    "message": f"Directory {directory} did not exist and was created. No files found yet."
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
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path) and file.lower().endswith(('.pdf', '.md', '.txt')):
                    doc_files.append(file_path)
                    
                    # Get file details
                    try:
                        file_size = os.path.getsize(file_path)
                        file_size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f} MB"
                        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
                        
                        file_details.append({
                            "name": file,
                            "path": file_path,
                            "size": file_size_str,
                            "modified": mod_time
                        })
                    except Exception as detail_error:
                        file_details.append({
                            "name": file,
                            "path": file_path,
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
                all_files = os.listdir(directory)
                if not all_files:
                    message = f"Directory {directory} is empty. No files found."
                else:
                    message = f"No PDF, MD, or TXT files found in {directory}. Directory contains {len(all_files)} other files."
            except:
                message = f"No PDF, MD, or TXT files found in {directory}."
                
            return {
                "status": "warning",
                "message": message,
                "suggestion": "Please upload document files or check another directory."
            }
        
        # Store in state for future reference
        tool_context.state["available_doc_files"] = doc_files
        tool_context.state["file_details"] = file_details
        
        return {
            "status": "success",
            "message": f"Found {len(doc_files)} document file(s) in {directory}",
            "doc_files": doc_files,
            "file_details": file_details
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Error finding document files: {str(e)}",
            "suggestion": "Please check if the directory exists and is accessible."
        }
def save_document_files_tool(tool_context, directory: str = "/tmp") -> Dict[str, Any]:
    try:
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

        for part in tool_context.user_content.parts:
            if hasattr(part, "inline_data") and part.inline_data and part.inline_data.data:
                mime = part.inline_data.mime_type
                file_data = part.inline_data.data

                # Determine file extension
                if mime == "application/pdf":
                    extension = ".pdf"
                elif mime == "text/markdown":
                    extension = ".md"
                elif mime == "text/plain":
                    extension = ".txt"
                else:
                    extension = ""

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                base_filename = f"document_{timestamp}"
                filename = f"{base_filename}{extension}"
                file_path = os.path.join(directory, filename)

                try:
                    if isinstance(file_data, str):
                        try:
                            decoded_data = base64.b64decode(file_data)
                            with open(file_path, 'wb') as f:
                                f.write(decoded_data)
                        except Exception:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(file_data)
                    else:
                        with open(file_path, 'wb') as f:
                            f.write(file_data)

                    file_size = os.path.getsize(file_path)
                    size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.1f} MB"

                    saved_files.append({
                        "name": filename,
                        "path": file_path,
                        "size": size_str,
                        "mime_type": mime
                    })

                except Exception as save_error:
                    error_files.append({
                        "name": filename,
                        "error": str(save_error)
                    })

        if saved_files:
            tool_context.state["saved_files"] = [f["path"] for f in saved_files]

            return {
                "status": "success",
                "message": f"Saved {len(saved_files)} file(s) to temporary directory.",
                "saved_files": saved_files,
                "error_files": error_files if error_files else None,
                "details": f"Files saved temporarily to: {directory}"
            }

        return {
            "status": "error",
            "message": "No valid files were saved.",
            "error_files": error_files if error_files else None
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
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
                "message": f"File not found: {file_path}",
                "suggestion": "Please check the file path or use find_file_tool to see available files."
            }
        
        # Check if file is readable
        if not os.access(file_path, os.R_OK):
            return {
                "status": "error",
                "message": f"File is not readable: {file_path}",
                "suggestion": "Please check file permissions."
            }
            
        # Read content based on file type
        if file_path.lower().endswith('.pdf'):
            try:
                # Read PDF content
                with open(file_path, 'rb') as pdf_file:
                    try:
                        pdf_reader = PdfReader(pdf_file)
                        content = ""
                        for page_num, page in enumerate(pdf_reader.pages):
                            content += f"\n--- Page {page_num + 1} ---\n"
                            page_text = page.extract_text()
                            if page_text:
                                content += page_text
                            else:
                                content += "[No extractable text on this page]"
                        
                        if not content.strip():
                            return {
                                "status": "warning",
                                "message": f"PDF file {file_path} appears to be empty or contains no extractable text.",
                                "content": "[No extractable text found in PDF]"
                            }
                    except Exception as pdf_error:
                        return {
                            "status": "error",
                            "message": f"Error parsing PDF file: {str(pdf_error)}",
                            "suggestion": "The PDF file may be corrupted or password-protected."
                        }
            except Exception as file_error:
                return {
                    "status": "error",
                    "message": f"Error opening PDF file: {str(file_error)}"
                }
                
        elif file_path.lower().endswith('.md') or file_path.lower().endswith('.txt'):
            try:
                # Try different encodings if UTF-8 fails
                encodings = ['utf-8', 'latin-1', 'cp1252']
                content = None
                
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as file:
                            content = file.read()
                        break  # If successful, exit the loop
                    except UnicodeDecodeError:
                        continue
                
                if content is None:
                    return {
                        "status": "error",
                        "message": f"Could not decode file with any of the attempted encodings: {encodings}",
                        "suggestion": "The file may be binary or use an unsupported encoding."
                    }
                    
                if not content.strip():
                    return {
                        "status": "warning",
                        "message": f"File {file_path} appears to be empty.",
                        "content": "[Empty file]"
                    }
            except Exception as file_error:
                return {
                    "status": "error",
                    "message": f"Error reading file: {str(file_error)}"
                }
        else:
            return {
                "status": "error",
                "message": f"Unsupported file type: {file_path}",
                "suggestion": "Only .pdf, .md, and .txt files are supported."
            }
        
        tool_context.state["extracted_content"] = content
        tool_context.state["document_processed"] = True
        tool_context.state["current_file"] = file_path
        
        content_length = len(content)
        if content_length > 1000:
            content_preview = content[:500] + "\n\n[...]\n\n" + content[-500:]
        else:
            content_preview = content
        
        return {
            "status": "success",
            "message": f"Successfully extracted content from {file_path}",
            "content_preview": content_preview,
            "total_length": content_length,
            "file_path": file_path
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
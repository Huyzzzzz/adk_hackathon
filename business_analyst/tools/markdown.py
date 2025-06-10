from datetime import datetime
from typing import Any, Dict
from pathlib import Path
from google.adk.tools import ToolContext
def json_to_markdown(data: Any) -> str:
    """
    Convert JSON data to Markdown format.

    Args:
        data: JSON data (dict, list, or any JSON-serializable object)

    Returns:
        Formatted Markdown string
    """
    markdown = f"*Generated on: {datetime.now().isoformat()}*\n\n"
    markdown += _convert_value(data, 0)
    return markdown


def _convert_value(value: Any, depth: int) -> str:
    """Convert a JSON value to Markdown format recursively."""
    indent = "  "
    indent_str = indent * depth

    if value is None:
        return "`null`"
    elif isinstance(value, bool):
        return f"`{str(value).lower()}`"
    elif isinstance(value, (int, float)):
        return f"`{value}`"
    elif isinstance(value, str):
        escaped = value.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`')
        return escaped
    elif isinstance(value, list):
        if not value:
            return "*(empty array)*"
        result = "\n"
        for item in value:
            result += f"{indent_str}- {_convert_value(item, depth + 1)}\n"
        return result
    elif isinstance(value, dict):
        if not value:
            return "*(empty object)*"
        result = "\n"
        for key, val in value.items():
            escaped_key = str(key).replace('*', '\\*').replace('_', '\\_')
            result += f"{indent_str}**{escaped_key}**: {_convert_value(val, depth + 1)}\n"
        return result
    else:
        return str(value)


def save_markdown_file(content: str, filename: str = "output.md", folder_path: str = "./") -> str:
    """
    Save markdown content to a file.

    Args:
        content: Markdown content to save
        filename: Name of the output file
        folder_path: Path to the folder where file should be saved

    Returns:
        Full path of the saved file
    """
    folder = Path(folder_path)
    file_path = folder / filename

    folder.mkdir(parents=True, exist_ok=True)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Markdown file saved to: {file_path.absolute()}")
        return str(file_path.absolute())
    except Exception as e:
        print(f"Error saving file: {e}")
        raise


def convert_and_save_json(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Convert state data from ToolContext to Markdown and save to file.

    Args:
        tool_context: ToolContext object containing state data

    Returns:
        Dictionary with success status, markdown content, and saved path
    """
    try:
        state_data = tool_context.state.to_dict()
        
        filename = f"AgentState_version_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
        markdown = json_to_markdown(state_data)
        saved_path = save_markdown_file(markdown, filename, "../assets/output/")
        
        return {
            "success": True,
            "markdown": markdown,
            "saved_path": saved_path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

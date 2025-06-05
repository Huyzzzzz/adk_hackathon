import os
from langchain_community.document_loaders import PyPDFLoader

def load_pdf_content(file_path: str):
    """
    Load all content from a PDF file using LangChain's PyPDFLoader.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        List[str]: List of text chunks extracted from the PDF.
    """
    # Initialize the PDF loader
    loader = PyPDFLoader(file_path)
    
    # Load and split the document into chunks
    documents = loader.load()
    
    # Extract text content from the document chunks
    content = [doc.page_content for doc in documents]

    # Define the output Markdown file path
    output_md_path = "../../assets/output/extracted_content.md"
    output_dir = os.path.dirname(output_md_path)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write content to a Markdown file
    with open(output_md_path, "w") as md_file:
        md_file.write("# Extracted Content from PDF\n\n")
        for i, page in enumerate(content):
            md_file.write(f"## Page {i + 1}\n\n")
            md_file.write(page + "\n\n")
    
    return content

# Example usage
if __name__ == "__main__":
    pdf_path = "/home/huytq132/adk_hackathon/assets/sample_data/RFI 2417LT Virtual Agent.pdf"  # Replace with the actual path to your PDF file
    pdf_content = load_pdf_content(pdf_path)
    for page in pdf_content:
        print(page)
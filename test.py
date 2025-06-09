import logging
from google.cloud import storage

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def download_file_from_gcs(bucket_name: str, file_path: str) -> str:
    """
    Downloads a file from Google Cloud Storage and returns its content as a string.

    Args:
        bucket_name (str): Name of the GCS bucket.
        file_path (str): Path to the file in the bucket.

    Returns:
        str: Content of the file.

    Raises:
        Exception: If the bucket or file does not exist, or if there are issues during download.
    """
    try:
        # Initialize the GCS client
        client = storage.Client()
        logging.info(f"Connecting to bucket: {bucket_name}")

        # Get the bucket
        bucket = client.get_bucket(bucket_name)
        logging.info(f"Bucket '{bucket_name}' accessed successfully.")

        # Get the blob (file)
        blob = bucket.blob(file_path)
        logging.info(f"Accessing file: {file_path}")

        # Check if the blob exists
        if not blob.exists():
            raise FileNotFoundError(f"File '{file_path}' does not exist in bucket '{bucket_name}'.")

        # Download the content
        content = blob.download_as_text()
        logging.info(f"File '{file_path}' downloaded successfully.")
        return content

    except Exception as e:
        logging.error(f"Error downloading file from GCS: {e}")
        raise

# Example usage
if __name__ == "__main__":
    bucket_name = "your-gcs-bucket-for-adk-artifacts"  # Replace with your bucket name
    file_path = "path/to/your/file.txt"  # Replace with your file path

    try:
        content = download_file_from_gcs(bucket_name, file_path)
        print("File Content:")
        print(content)
    except Exception as e:
        print(f"Failed to download file: {e}")
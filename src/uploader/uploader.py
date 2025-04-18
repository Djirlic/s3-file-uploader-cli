import requests
from requests.exceptions import RequestException

from uploader.logger import logger


def upload_file_to_presigned_url(presigned_url: str, file_path: str) -> bool:
    """
    Upload a file to S3 using a presigned URL.

    Args:
        presigned_url (str): Presigned URL for uploading the file.
        file_path (str): Local path to the file to upload.

    Returns:
        bool: True if upload was successful, False otherwise.
    """
    try:
        with open(file_path, "r+b") as file:
            logger.info("🚀 Uploading file to presigned URL...")
            response = requests.put(presigned_url, data=file)
            logger.info(f"📬 S3 responded with status code: {response.status_code}")

            if response.status_code == 200:
                return True
            else:
                logger.warning(f"⚠️ Upload failed with {response.status_code}: {response.text}")
                return False
    except FileNotFoundError:
        logger.error(f"❌ File not found: {file_path}")
    except PermissionError:
        logger.error(f"❌ Permission denied when accessing file: {file_path}")
    except RequestException as e:
        logger.error(f"❌ Network or HTTP error during upload: {e}")
    except Exception as e:
        logger.exception(f"❌ Unexpected error during file upload: {e}")

    return False

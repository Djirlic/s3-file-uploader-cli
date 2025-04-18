import requests

from uploader.logger import logger


def upload_file_to_presigned_url(presigned_url: str, file_path: str) -> bool:
    try:
        with open(file_path, "r+b") as file:
            logger.info("🚀 Uploading file to presigned URL...")
            http_response = requests.put(presigned_url, data=file)
            logger.info(f"📬 S3 responded with status code: {http_response.status_code}")
            return http_response.status_code == 200
    except Exception as e:
        logger.error(f"❌ Error during upload: {e}")
        return False

import pytest
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound

from uploader.presigner import get_presigned_url, get_s3_client


def test_get_s3_client_returns_client_object(mocker):
    mock_session = mocker.Mock()
    mock_client = mocker.Mock()
    mock_session.client.return_value = mock_client
    mocker.patch("uploader.presigner.boto3.Session", return_value=mock_session)

    client = get_s3_client("default")

    assert client is mock_client
    mock_session.client.assert_called_once_with("s3")


def test_get_presigned_url_with_invalid_profile_returns_none(mocker):
    mocker.patch(
        "uploader.presigner.boto3.Session", side_effect=ProfileNotFound(profile="invalid_profile")
    )

    result = get_presigned_url(
        bucket_name="test-bucket", upload_path="some/path.csv", profile="invalid_profile"
    )

    assert result is None


@pytest.mark.parametrize(
    "error",
    [
        ClientError(
            error_response={"Error": {"Code": "AccessDenied", "Message": "Access Denied"}},
            operation_name="GeneratePresignedUrl",
        ),
        Exception("Some other error"),
        BotoCoreError(),
    ],
)
def test_get_presigned_url_with_client_error_returns_none(mocker, error):
    mock_client = mocker.Mock()
    mock_client.generate_presigned_url.side_effect = error

    mocker.patch("uploader.presigner.get_s3_client", return_value=mock_client)

    result = get_presigned_url(
        bucket_name="test-bucket", upload_path="some/path.csv", profile="default"
    )

    assert result is None


def test_get_presigned_url_returns_url(mocker):
    mock_client = mocker.Mock()
    mock_client.generate_presigned_url.return_value = "https://example.com/presigned"

    mocker.patch("uploader.presigner.get_s3_client", return_value=mock_client)

    result = get_presigned_url(
        bucket_name="test-bucket", upload_path="some/path.csv", profile="default"
    )

    assert result == "https://example.com/presigned"

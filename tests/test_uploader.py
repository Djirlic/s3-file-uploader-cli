import pytest
import requests

from uploader.uploader import upload_file_to_presigned_url


def test_upload_file_to_presigned_url_with_file_not_found_error_returns_false(mocker):
    mocker.patch("builtins.open", side_effect=FileNotFoundError)

    result = upload_file_to_presigned_url(
        presigned_url="https://example.com/presigned-url", file_path="non_existent_file.txt"
    )

    assert result is False


def test_upload_file_to_presigned_url_with_permission_error_returns_false(mocker):
    mocker.patch("builtins.open", side_effect=PermissionError)

    result = upload_file_to_presigned_url(
        presigned_url="https://example.com/presigned-url",
        file_path="file_with_no_permissions_to.txt",
    )

    assert result is False


def test_upload_file_to_presigned_url_with_requests_exception_returns_false(mocker):
    mocker.patch("requests.put", side_effect=requests.exceptions.RequestException)
    mocker.patch("builtins.open", mocker.mock_open(read_data="dummy data"))

    result = upload_file_to_presigned_url(
        presigned_url="https://example.com/presigned-url", file_path="file.txt"
    )

    assert result is False


def test_upload_file_to_presigned_url_with_other_exception_returns_false(mocker):
    mocker.patch("requests.put", side_effect=Exception("Some other error"))
    mocker.patch("builtins.open", mocker.mock_open(read_data="dummy data"))

    result = upload_file_to_presigned_url(
        presigned_url="https://example.com/presigned-url", file_path="file.txt"
    )

    assert result is False


@pytest.mark.parametrize(
    "status_code, expected",
    [
        (200, True),
        (403, False),
        (500, False),
    ],
)
def test_upload_file_to_presigned_url_with_various_status_codes(mocker, status_code, expected):
    mock_response = mocker.Mock()
    mock_response.status_code = status_code
    mocker.patch("requests.put", return_value=mock_response)
    mocker.patch("builtins.open", mocker.mock_open(read_data="some, csv, data"))

    result = upload_file_to_presigned_url(
        presigned_url="https://example.com/presigned-url", file_path="file.csv"
    )

    assert result is expected

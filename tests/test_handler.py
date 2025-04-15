from uploader.handler import handler

def test_handler_with_empty_body_fails_with_400():
  event = {
    "body": "",
    "headers": {
      "Content-Type": "text/csv"
    }
  }

  response = handler(event, None)
  assert response['statusCode'] == 400
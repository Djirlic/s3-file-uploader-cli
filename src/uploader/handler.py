def handler(event, content):
    if event.get("body") == "":
        response = {
            "statusCode": 400,
            "body": {
                "error": "Bad request",
                "message": "Request body could not be read properly.",
            },
        }
        return response


def handler(event, content):
    if event.get("body") == "":
      response = {
        "statusCode": 400,
        "body": ""
    }
    return response


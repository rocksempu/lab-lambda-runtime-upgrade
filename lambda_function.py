import json
import sys
import platform

def handler(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "message": "Hello from Lambda!",
            "python_version": sys.version,
            "platform": platform.platform(),
        }),
    }

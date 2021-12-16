import requests
import json
import os

class SlackNotice:
    def __init__(self):
        pass


    def post(self, payload):
        url = os.environ.get("ABYSSWATCHER_SLACK_ENDPOINT", None)
        headers = {"Content-Type": "application/json"}

        try:
            req = requests.post(url, headers=headers, data=json.dumps({"text":payload}))
            return {"msg":"success!"}
        except:
            return {"msg":"error!"}
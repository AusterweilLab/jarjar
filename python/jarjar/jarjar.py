import requests
import json

class jarjar():
    def __init__(self, channel, url="your-webhook-here"):
        self.channel = channel
        self.url = url
        self.headers ={'Content-Type': 'application/json'}
    def post(self, text):
        payload = json.dumps({"text": text, "channel": self.channel})
        response = requests.post(self.url,data=payload,headers=self.headers)
        return response

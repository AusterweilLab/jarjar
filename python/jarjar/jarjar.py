import requests
import json

class jarjar():
    def __init__(self, url):
        self.url = url
        self.headers ={'Content-Type': 'application/json'}
        
    def post(self, text, channel):
        payload = json.dumps({"text": text, "channel": channel})
        response = requests.post(self.url,data=payload,headers=self.headers)
        return response


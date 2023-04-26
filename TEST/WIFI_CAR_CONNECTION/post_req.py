import json
import requests

data = {"path_id": "0"}
headers = {"Content-Type": "application/json"}


response = requests.post("http://192.168.1.66/goTo", data=json.dumps(data), headers=headers)
#response = requests.get("http://pigrinatorcar/")
#response = requests.post("http://esp32/followThisPath", data=json.dumps(data), headers=headers)
print(response)
import json
import requests

# data = {"path_id": "0"}
data = {"path": [{"direction": "forward", "value": 150}, {"direction": "right", "value": 90}]}
headers = {"Content-Type": "application/json"}


#response = requests.post("http://192.168.1.66/goTo", data=json.dumps(data), headers=headers)
#response = requests.get("http://pigrinatorcar/")
#response = requests.post("http://esp32/followThisPath", data=json.dumps(data), headers=headers)




# response = requests.put("http://192.168.1.66/newPath", data=json.dumps(data), headers=headers)
response = requests.get("http://192.168.1.66/searchPath/4")


print(response.json())
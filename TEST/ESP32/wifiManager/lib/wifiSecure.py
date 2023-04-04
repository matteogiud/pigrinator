import json

def readFile():
    try:
        with open('lib/wifiSecure.json', 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(e)
        
def loadWifi(SSID, PSW) -> None:
    try:
        with open('lib/wifiSecure.json', 'r') as file:
            data = json.load(file)
                    
        data['wifi'].append(dict(ssid=SSID, psw=PSW))
        
        with open('lib/wifiSecure.json', 'w') as file:
            json.dump(data, file)
        print(data)

    except Exception as e:
        print(e)
    

def search(SSID) -> str:
    try:
        with open('lib/wifiSecure.json', 'r') as file:
            data = json.load(file)
        for wifi in data['wifi']:
            if wifi['ssid'] == SSID:
                return wifi['psw']
        return None
    except Exception as e:
        return None
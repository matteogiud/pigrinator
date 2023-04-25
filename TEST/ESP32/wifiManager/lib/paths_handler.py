import json

def readFile():
    try:
        with open('paths.json', 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(e)
        
def loadWifi(paths={}) -> None:
    try:
        with open('lib/wifiSecure.json', 'r') as file:
            data = json.load(file)
        
        new_id = max(map(int, data['paths'].keys())) + 1
        
              
        data[str(new_id)]= paths
        
        with open('lib/wifiSecure.json', 'w') as file:
            json.dump(data, file)
        print(data)

    except Exception as e:
        print(e)
    

def search(path_id) -> str:
    try:
        with open('lib/wifiSecure.json', 'r') as file:
            data = json.load(file)
            
        return data["paths"][str(path_id)]
    except Exception as e:
        return None


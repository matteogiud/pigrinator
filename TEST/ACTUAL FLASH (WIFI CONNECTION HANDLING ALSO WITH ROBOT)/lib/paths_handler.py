import json


def readFile():
    try:
        with open('paths.json', 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(e)


def loadPath(path={}) -> bool:
    if not checkPath(path=path):
        return -1
    try:
        with open('paths.json', 'r') as file:
            data = json.load(file)

        new_id = max(map(int, data['paths'].keys())) + 1

        data['paths'][str(new_id)] = path

        with open('paths.json', 'w') as file:
            json.dump(data, file)
            
        print("[load path] path loaded")
        
        return new_id

    except Exception as e:
        print(e)
        return -1
    
def checkPath(path={}):
    if not path:
        return False
    valid_keys = ("forward", "backward", "left", "right")
    try:           
        # x:dict = {"forward": 100}
        for step in path:
            if not len(step) == 2:
                return False
            
            if not all(key in step for key in ["direction", "value"]):
                return False
            
            direction = step["direction"]
            if direction not in ["forward", "backward", "left", "right"]:
                return False
            
            value = step["value"]
            if not isinstance(value, int) or value <= 0:
                return False            
            
    except:
        return False
    
    return True

def search(path_id) -> str:
    try:
        with open('paths.json', 'r') as file:
            data = json.load(file)

        return data["paths"][str(path_id)]
    except Exception as e:
        print("[paths_handler]: ", e)
        return None
    
def search_all() -> str:
    try:
        with open('paths.json', 'r') as file:
            data = json.load(file)

        return data["paths"]
    except Exception as e:
        print("[paths_handler]: ", e)
        return None

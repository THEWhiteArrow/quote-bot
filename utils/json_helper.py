import json
import os

def read_json(filename:str=''):
    with open(filename, "r") as f:
        return json.load(f)
    
def write_json(filename:str='', json_data:dict=None):
    with open(filename, "w") as f:
        json.dump(json_data, f , indent=4,)

def check_json(filename:str=''):
    if not os.path.exists(filename):
        write_json(filename, {})

def exists_json(filename:str=''):
    return os.path.exists(filename)

def invalid_json(filename:str=''):
    try:
        read_json(filename)
        return False
    except:
        return True
import json 
import os 
from utils.toml_helper import *
from utils.json_helper import *
from utils.quote_helper import *
from quotes.zenquotes import get_zenquotes
 

def get_quotes():   
    config = read_toml()
    quote_history_filename = "./quote_history.json"
    
    if not exists_json(quote_history_filename) or invalid_json(quote_history_filename):
        print("Creating quote history file")
        write_json(quote_history_filename, {"quotes": []})
    
    history = read_json(quote_history_filename)
    
 
    if config["app"]["status"] == "dev":
        quotes = [Quote("Hello World text to speech", "Unknown",1691932240)]
    else:
        quotes = get_zenquotes(config["quotes"]["min_length"], config["quotes"]["max_length"])
    
        quotes = [q for q in quotes if not q in history["quotes"]]
        
        history["quotes"] = [*history["quotes"], *[q.__dict__() for q in quotes]]
    
        write_json(quote_history_filename, history) 

    return quotes
    

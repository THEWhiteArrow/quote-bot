import json 
import os
import time 

from quotes.zenquotes import get_zenquotes


def get_quotes(min_length:int=75, max_length:int=100): 
    quotes = get_zenquotes(min_length, max_length)
    filename = "used_quotes.json"

    # if os.path.exists(filename):
    #     with open(filename, "w") as f:
    #         used_quotes = json.load(f)
    #         quotes = [q for q in quotes if q not in used_quotes]
    # else:
    #     # Create an empty dictionary if the file doesn't exist
    #     with open(filename, "w") as file:
    #         json.dump(quotes, file)
    #     print("Created a new file:", filename)

    # return quotes

    if os.path.exists(filename):
        quote_elements = json.load(open(filename)) 
        loaded_quotes = [el.quote for el in quote_elements["quotes"] ]
        quotes = [q for q in quotes if q not in loaded_quotes]
    else:
        quote_elements = {"quotes": quotes}
1 
    

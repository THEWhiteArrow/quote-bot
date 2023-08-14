import time
from uuid import uuid4

class Quote:
    quote : str = ""
    author : str = ""
    id : int = 0

    def __init__(self, quote, author, id:str = str(uuid4()) ):
        self.quote = quote
        self.author = author
        self.id = id
       
    def __eq__(self, other):
        if not isinstance(other, Quote):
            try:
                other = Quote(other["quote"], other["author"], other["id"])
            except:
                return False
            
        return self.quote == other.quote and self.author == other.author
 
    
    def __dict__(self):
        return {
            "quote": self.quote,
            "author": self.author,
            "id": self.id
        }

    def __json__(self):
        return {
            "quote": self.quote,
            "author": self.author,
            "id": self.id
        }
    
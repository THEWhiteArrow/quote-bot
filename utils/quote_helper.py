import time

class Quote:
    quote : str = ""
    author : str = ""
    timestamp : int = 0

    def __init__(self, quote, author, timestamp:int = int(time.time())):
        self.quote = quote
        self.author = author
        self.timestamp = timestamp
       
    def __eq__(self, other):
        if not isinstance(other, Quote):
            try:
                other = Quote(other["quote"], other["author"], other["timestamp"])
            except:
                return False
            
        return self.quote == other.quote and self.author == other.author
 
    
    def __dict__(self):
        return {
            "quote": self.quote,
            "author": self.author,
            "timestamp": self.timestamp
        }

    def __json__(self):
        return {
            "quote": self.quote,
            "author": self.author,
            "timestamp": self.timestamp
        }
    
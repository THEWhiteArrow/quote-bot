from utils.json_helper import *
from uuid import uuid4


class Quote:
    quote: str = ""
    author: str = ""
    id: str = ""

    def __init__(self, quote, author):
        self.quote = quote
        self.author = author
        self.id = str(uuid4())

    def __eq__(self, other):
        if not isinstance(other, Quote):
            try:
                other = Quote(other["quote"], other["author"])
            except:
                return False

        return self.quote == other.quote and self.author == other.author

    def __dict__(self):
        return {"quote": self.quote, "author": self.author, "id": self.id}

    def __json__(self):
        return {"quote": self.quote, "author": self.author, "id": self.id}


def save_quote_to_history(q: Quote):
    if invalid_json("history.json"):
        write_json("history.json", {"quotes": []})

    history = read_json("history.json")
    history["quotes"].append(q.__dict__())

    write_json("history.json", history)

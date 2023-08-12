import requests

def get_zenquotes(min_length:int=75, max_length:int=100):
    url = 'https://zenquotes.io/api/quotes'
    saved_quotes = []

    response = requests.get(url)
    quotes = response.json()
    for q in quotes: 
        if int(q['c']) >= min_length and int(q['c']) <= max_length:
            saved_quotes.append(q['q'])

    return saved_quotes
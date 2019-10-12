import requests
import json

baseURI = 'https://api.exchangeratesapi.io/latest?base=%s&symbols=EUR'

def getRate(currency):
    response = json.loads(requests.get(baseURI % currency).content)
    return response['rates']['EUR']

if __name__ == "__main__":
    print(getRate('GBP'))

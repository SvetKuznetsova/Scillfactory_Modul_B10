import json
import requests
from config import exchanges

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            quote_ticker = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f'Неверное наименование валюты "{quote}"')

        try:
            base_ticker = exchanges[base.lower()]
        except KeyError:
            raise APIException(f'Неверное наименование валюты "{base}"')

        if quote_ticker == base_ticker:
            raise APIException(f'Введена одинаковая валюта "{base}"')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Уточните количество "{amount}"')
        
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        resp = json.loads(r.content)
        new_price = resp[exchanges[base]] * amount
        new_price = round(new_price, 2)
        message = f"Цена {amount} {quote} в {base} : {new_price}"
        return message

import json
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def api(frm,to):
    url= "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol={}&convert={}&CMC_PRO_API_KEY='70b558a8-8ad0-4d2b-8e9f-559cc06fdcd3'".format(frm, to)

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '70b558a8-8ad0-4d2b-8e9f-559cc06fdcd3',}

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    print("SEPARADOR")
    print(data['data']['quote'][to]['price'])

    return data

api("EUR","BTC")

import requests

DH_HOST = 'dinning_hall'


def fetch_kitchen_data_from_dh(port):
    res = requests.get(f'http://{DH_HOST}:{port}/restaurant_data')
    json_ = res.json()
    return json_['config']
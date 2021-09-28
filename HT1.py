  
import requests
import json
import os

from datetime import date

from requests.exceptions import HTTPError
from config import Config


def login(config):
    url = config['url']+config['auth_point']
    headers = {"content-type": "application/json"}
    data = {"username": config['username'], "password": config['password']}
    try:
        r = requests.post(url, headers=headers, data=json.dumps(data))
        r.raise_for_status()
        token = r.json()['access_token']
        
        return token

    except HTTPError:
        print ("HTTP Error")
        return False
    except Exception:
        print ("Error")
        return False
        
def getdata(config, token, process_date=None):
    if not process_date:
        process_date = str(date.today())
    url = config['url']+config['data_point']
    
    headers = {"content-type": "application/json", "Authorization": "JWT " + token}
    data = {"date": str(process_date)}
    try:
        r = requests.get(url, headers=headers, data=json.dumps(data))
        r.raise_for_status()
        os.makedirs(os.path.join(config['directory'], process_date), exist_ok=True)
        with open(os.path.join(config['directory'], process_date, str(process_date)+'.json'), 'w') as json_file:
            data = r.json()
            json.dump(data, json_file)

    except HTTPError:
        print(F"Http Error at date {process_date}")


if __name__ == '__main__':
    config = Config(os.path.join('.', 'config.yaml'))
    config = config.get_config('HT1_app')
    token = login(config)
    if token!=False:
        
        date = ['2025-06-24', '2021-06-19', '2021-06-20', '2021-06-21']
        for dt in date:
            getdata(config,token,dt)
    
import requests
import json


def create_elastic_index():

    url = "http://localhost:9200/inventory"
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {"settings": {"number_of_shards": 1},
               "mappings": {"properties": {"servers": {"type": "long"}}}}

    response = requests.request("PUT", url,headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print(response.text)
    else:
        print("Inventory index already exists")


def populate_inventory():
    dc_servers = {"amazon": 850, "michigan": 904, "rhino": 1208, "tahoe": 150}
    for dc in dc_servers.keys():
        url = "http://localhost:9200/inventory/_doc/{}/".format(dc)
        headers = {'Content-Type': 'application/json'}
        payload = {"servers": dc_servers[dc]}
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        print(response.text.encode('utf8'))

############################################################
#
#
#
#
#
#
#
############################################################

import requests
import json


def Model(root,NUTS,BRANDS,SUPPLY,PRICE,FORMULA,PRODUCE,STATUS):

    url = f"{root}/model/"
    payload = json.dumps({"LINGO_script": "chess.lng"})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    MODEL_ID = response.json()["model_id"]

    url = f"{root}/pointer/"
    payload = json.dumps([
    {
        "pointer_pos": 1,
        "model_id": MODEL_ID,
        "pointer_name": "NUTS",
        "pointer_type": "SET",
        "pointer_data": NUTS
    },
    {
        "pointer_pos": 2,
        "model_id": MODEL_ID,
        "pointer_name": "BRANDS",
        "pointer_type": "SET",
        "pointer_data": BRANDS
    },
    {
        "pointer_pos": 3,
        "model_id": MODEL_ID,
        "pointer_name": "SUPPLY",
        "pointer_type": "PARAM",
        "pointer_data": SUPPLY
    },
    {
        "pointer_pos": 4,
        "model_id": MODEL_ID,
        "pointer_name": "PRICE",
        "pointer_type": "PARAM",
        "pointer_data": PRICE
    },
    {
        "pointer_pos": 5,
        "model_id": MODEL_ID,
        "pointer_name": "FORMULA",
        "pointer_type": "PARAM",
        "pointer_data": FORMULA
    },
    {
        "pointer_pos": 6,
        "model_id": MODEL_ID,
        "pointer_name": "PRODUCE",
        "pointer_type": "VAR",
        "pointer_data": PRODUCE
    },
    {
        "pointer_pos": 7,
        "model_id": MODEL_ID,
        "pointer_name": "STATUS",
        "pointer_type": "VAR",
        "pointer_data": STATUS
    }
    ])
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)

    url = f"{root}/solve/{MODEL_ID}/"
    payload = ""
    headers = {}
    response = requests.request("PUT", url, headers=headers, data=payload)

    url = f"{root}/model_pointer/{MODEL_ID}/"
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = response.json()

    errorMessage = response_json['errorMessage']
    PRODUCE = response_json['pointers'][5]['pointer_data']
    STATUS = response_json['pointers'][6]['pointer_data']

    return errorMessage, PRODUCE, STATUS




def main():

    root = 'http://localhost:8000'

    NUTS    = ["Peanut","Cashew"]
    BRANDS  = ["Pawn","Knight","Bishop","King"]
    SUPPLY  = [750, 250]
    PRICE   = [2, 3, 4, 5]
    FORMULA = [ 15, 10,  6,  2,
                1,  6, 10, 14]
    PRODUCE = [0, 0, 0, 0]
    STATUS  = [0]

    try:

        errorMessage, PRODUCE, STATUS = Model(root,NUTS,BRANDS,SUPPLY,PRICE,FORMULA,PRODUCE,STATUS)
        if errorMessage == "NONE":
            for i in range(0,len(BRANDS)):
                print(f"{BRANDS[i]:10} {PRICE[i]:5} {float(PRODUCE[i]):10.2f}")
        print(STATUS)

    except Exception as e:

        print(e)


if __name__ == "__main__":
    main()
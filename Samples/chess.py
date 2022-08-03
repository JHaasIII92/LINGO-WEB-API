"""
In blending problems, two or more raw materials are to be blended into one or more 
finished goods, satisfying one or more quality requirements on the finished goods.
In this example, the Chess Snackfoods Co. markets four brands of mixed nuts. 
Each brand contains a specified ration of peanuts and cashews. 
Chess has contracts with suppliers to receive 750 pounds of peanuts/day and 250 
pounds of cashews/day. The problem is to determine the number of pounds of each brand
to produce each day to maximize total revenue without exceeding the available supply
of nuts.

max p'x
st Fx <= b
x >= 0

p - price that each brand sells for
F - formula matrix F_ij number of nut_i needed in brand_j
b - supply of each type of nut
x - amount of each brand to produce

Output: print out

Global optimum found!
Brand      Peanut       Cashew     Produce
==========================================
Pawn         721.1538    48.0769   769.2308
Knight         0.0000     0.0000     0.0000
Bishop         0.0000     0.0000     0.0000
King          28.8462   201.9231   230.7692
==========================================
Totals          750.0      250.0     1000.0


To run have the LINGO demo server running localy.
Then run the command:
py path\to\Samples\chess.py

The API root is set to root='http://localhost:8000' by defualt in main function.



"""
import requests
import json
import numpy as np

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
        "pointer_data": NUTS.tolist()
    },
    {
        "pointer_pos": 2,
        "model_id": MODEL_ID,
        "pointer_name": "BRANDS",
        "pointer_type": "SET",
        "pointer_data": BRANDS.tolist()
    },
    {
        "pointer_pos": 3,
        "model_id": MODEL_ID,
        "pointer_name": "SUPPLY",
        "pointer_type": "PARAM",
        "pointer_data": SUPPLY.tolist()
    },
    {
        "pointer_pos": 4,
        "model_id": MODEL_ID,
        "pointer_name": "PRICE",
        "pointer_type": "PARAM",
        "pointer_data": PRICE.tolist()
    },
    {
        "pointer_pos": 5,
        "model_id": MODEL_ID,
        "pointer_name": "FORMULA",
        "pointer_type": "PARAM",
        "pointer_data": (FORMULA.flatten()).tolist()
    },
    {
        "pointer_pos": 6,
        "model_id": MODEL_ID,
        "pointer_name": "PRODUCE",
        "pointer_type": "VAR",
        "pointer_data": PRODUCE.tolist()
    },
    {
        "pointer_pos": 7,
        "model_id": MODEL_ID,
        "pointer_name": "STATUS",
        "pointer_type": "VAR",
        "pointer_data": STATUS.tolist()
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
    PRODUCE = np.array(response_json['pointers'][5]['pointer_data'],dtype=np.double)
    STATUS = np.array(response_json['pointers'][6]['pointer_data'],dtype=np.double)

    return errorMessage, PRODUCE, STATUS




def main():

    root='https://lingo-api-demo.com'

    NUTS    = np.array(["Peanut","Cashew"])
    peanut_i   = 0
    cashew_i   = 1
    BRANDS  = np.array(["Pawn","Knight","Bishop","King"])
    BRAND_COUNT = len(BRANDS)
    SUPPLY  = np.array([750, 250])
    PRICE   = np.array([2, 3, 4, 5])
    FORMULA = np.array([[ 15, 10,  6,  2],
                        [1,  6, 10, 14]])
    PRODUCE = np.array([0, 0, 0, 0])
    STATUS  = np.array([-1])

    try:

        errorMessage, PRODUCE, STATUS = Model(root,NUTS,BRANDS,SUPPLY,PRICE,FORMULA,PRODUCE,STATUS)
        if errorMessage == "NONE":
            
            # display the blend
            totalPeanuts = np.sum(PRODUCE*FORMULA[peanut_i]/16)
            totalCashew  = np.sum(PRODUCE*FORMULA[cashew_i]/16)
            totalProduced = np.sum(PRODUCE)
            print(f"Brand      Peanut       Cashew     Produce")
            print(f"==========================================")
            for i in range(0,BRAND_COUNT):
                peanuts = PRODUCE[i]*FORMULA[peanut_i,i]/16
                cashews = PRODUCE[i]*FORMULA[cashew_i,i]/16
                print(f"{BRANDS[i]:10} {peanuts:10.4f} {cashews:10.4f} {PRODUCE[i]:10.4f}")
            print(f"==========================================")
            print(f"{'Totals':10} {totalPeanuts:10} {totalCashew:10} {totalProduced:10}")
        else:
            print(errorMessage)
    except Exception as e:

        print(e)


if __name__ == "__main__":
    main()
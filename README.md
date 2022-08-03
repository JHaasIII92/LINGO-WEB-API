# LINGO REST API DEMO

## Introduction 

The LINGO REST API makes LINGO accessible on a variety of languages and devices by hosting LINGO on a server. This guide will go through setting up the API locally, creating and solving models, and some more advanced topics.

To see webaplications connected to a LINGO REST server see the following links:

https://tsp.lingo-api-demo.com/

https://staff-schedule.lingo-api-demo.com/

## Setting Up A Demo Server

A LINGO REST API server can be run locally on your computer with Docker. To get started download [Docker and Docker Compose](https://docs.docker.com/compose/install/).  Next download the LINGO-WEB-API repository. In the command line open to the LINGO-WEB-API directory and run the following command:

```bash
docker pull lindosystems/lingorestdemo
doker-compose run LINGO_API python manage.py makemigrations LINGO_REST
docker-compose run LINGO_API python manage.py migrate
docker-compose up
```

## Overview

After setting up the LINGO API server, the chess.lng file will be the focus of this guide. The cURL programing language will be used throughout the documentation, and the code here can be ran on the command line with some modifications.

The URL `http://localhost/`is used in each of the cURL commands and is the root of the API when it is running locally. After the root of the API there are six extensions:

1. **model**:  Create models
2. **pointer**: Create pointers
3. **solve**: Tell the API to solve a model. 
4. **model_pointer**: Get a model and each of its pointers
5. **file**: Upload files
6. **log**: Download logs

## Model Creation

The first step when using the LINGO REST API is to make a POST request to create an instance of a model. The one field that is required to create a model is `LINGO_script`, which must be a LINGO `.lng` file that is on the server. The model, chess.lng will already be on the server, see the section **Adding Models** for information on adding your own LINGO models. The following cURL command creates a new chess model:
``` curl
curl --location --request POST 'http://localhost:8000/model/' \
--header 'Content-Type: application/json' \
--data-raw '{"LINGO_script":"chess.lng"}'
```
On a successful post the response data should look like the JSON object below, otherwise, the HTTP status 400 was returned:
```
{
"model_id": MODEL_ID,
"errorMessage": "",
"LINGO_script": "chess.lng",
"model_cb": false
}
```

The `model_id` field is important since it is used to attached pointer data where {MODEL_ID} appears in the documentation when running the command. Replace it with the actual MODEL_ID returned when creating a model. This will be an integer. The other two fields that were not defined in the cURL command are `errorMessage` which will attach any error message that was returned when solving the model and `model_cb` which is by default false, however, could have been set to true for callback data please. See the **Callback** section for more information.


## Adding Data
After the model has been created, add data to it by using a POST request on pointer. There are five fields that are needed to describe a pointer:

1. **pointer_pos**: The index of the pointer in the LINGO `.lng` file. 
2.  **model_id**:  The model ID number that the pointer data is being written to. The `model_id` is returned when the model is created, see previous section.
3. **pointer_name**:  A name to describe the purpose of the pointer. 
4. **pointer_type**: There are three types of pointers:
	- SET: This type is meant to initialize elements of a set with string names or enumeration.
	- PARAM: This type of pointer is parameter data that is fixed for this instance of the model
	- VAR: This type indicates that the pointer data is a variable in the model
5. **pointer_data**:  An array of data that will be sent to LINGO. If the pointer type is SET, then the data can be string or integer. Otherwise, the data must be floating point or integer. The pointers with VAR data must be allocated with enough elements to fill in all its final data

The following cURL command creates the SET BRANDS in the`chess.lng` model. This pointer corresponds to the second pointer in the model, so its `pointer_pos` is 2. This pointer has `pointer_type` of SET, so it is `pointer_data` and can be an array of string.

```curl
curl --location --request POST 'http://localhost:8000/pointer/' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
        "pointer_pos": 1,
        "model_id": {MODEL_ID},
        "pointer_name": "BRANDS",
        "pointer_type": "SET",
        "pointer_data": ["Pawn","Knight","Bishop","King"]
    }
]'
```

The next cURL command adds the price of each brand in the `chess.lng` model. It is the fourth pointer in the model, so its `pointer_pos` is 4. The price data is fixed, so it is type PARAM. There are four brands in this instance of the `chess.lng` model, so there are four prices in the `pointer_data` array.

```curl
curl --location --request POST 'http://localhost:8000/pointer/' \
--header 'Content-Type: application/json' \
--data-raw '[
	{
	    "pointer_pos": 4,
	    "model_id": {MODEL_ID},
	    "pointer_name": "PRICE",
	    "pointer_type": "PARAM",
	    "pointer_data": [2.0,3.0,4.0,5.0]
	}
]'
```

The next cURL command allocates memory for the number of each brand to produce after the model has been solved. It is the sixth pointer in the model, so its `pointer_pos` is 6. The produce data is a decision variable, so it is type VAR. There are four brands in this instance of `chess.lng` model, so the `pointer_data` needs to have four elements.

```curl
curl --location --request POST 'http://localhost:8000/pointer/' \
--header 'Content-Type: application/json' \
--data-raw '[
	{
	    "pointer_pos": 6,
	    "model_id": {MODEL_ID},
	    "pointer_name": "PRODUCE",
	    "pointer_type": "VAR",
	    "pointer_data": [0,0,0,0]
	},
]'
```
It is best to send all the data to the model at once. Doing so will decrease the run.

## Calling LINGO

Once all the pointer data have been added to the model, make a PUT request to solve.
  
```curl
curl --location --request PUT 'http://localhost:8000/solve/{MODEL_ID}/'
```

## Querying Results 

To get the model data after the LINGO API has solved the model you can use a GET request on `model_pointer` to get all the model data:

```curl
curl --location --request GET 'http://localhost:8000/model_pointer/{MODEL_ID}/'
```

If run successfully, the chess model will return something like this:

```
{"model_id":{MODEL_ID},"LINGO_script":"chess.lng","errorMessage":"NONE","model_cb":false,
"pointers":[{"id":15,"pointer_pos":1,"model_id":{MODEL_ID},"pointer_name":"NUTCOUNT","pointer_type":"SET","pointer_data":["Peanut","Cashew"]},
{"id":16,"pointer_pos":2,"model_id":{MODEL_ID},"pointer_name":"BRANDCOUNT","pointer_type":"SET","pointer_data":["Pawn","Knight","Bishop","King"]},
{"id":17,"pointer_pos":3,"model_id":{MODEL_ID},"pointer_name":"SUPPLY","pointer_type":"PARAM","pointer_data":["750","250"]},
{"id":18,"pointer_pos":4,"model_id":{MODEL_ID},"pointer_name":"PRICE","pointer_type":"PARAM","pointer_data":["2","3","4","5"]},
{"id":19,"pointer_pos":5,"model_id":{MODEL_ID},"pointer_name":"FORMULA","pointer_type":"PARAM","pointer_data":["15","10","6","2","1","6","10","14"]},
{"id":20,"pointer_pos":6,"model_id":{MODEL_ID},"pointer_name":"PRODUCE","pointer_type":"VAR","pointer_data":["769.2307692307693","0.0","0.0","230.76923076923075"]},
{"id":21,"pointer_pos":7,"model_id":{MODEL_ID},"pointer_name":"STATUS","pointer_type":"VAR","pointer_data":["0.0"]}]
}
```

The above JSON object is a join on the model object and each of the models’ attached pointers. The field `errorMessage` is now filled in and is "NONE" if no errors were returned otherwise a detailed error message will be in there.

## Adding Models

To add a model to the API server, use cURL to provide a LINGO `.lng` file and a file name. The two fields in the request are as follows:

1. **lng_file**: The absolute path to the LINGO model file
2. **lng_name**: The name of the file with the `.lng` extension. 
``` cURL
curl --location --request POST 'http://localhost:8000/file/' \
-F lng_file=@"path/to/MODEL.lng" \
-F lng_name="MODEL.lng"
```

## Callback 

To turn on the callback option make a POST request to callback, and set `callback_id` to the MODEL_ID before solving the model. 

``` curl
curl --location --request POST 'http://localhost:8000/callback/' \
--header 'Content-Type: application/json' \
--data-raw '{"callback_id":{MODEL_ID}}'
```

While the solver is running in the background make GET requests to callback 

```curl
curl --location --request GET 'http://localhost:8000/callback/{MODEL_ID}'
```

The GET request will return a JSON object with the fields

1. **callback_id**: This will be the same as the MODEL_ID.
2. **HTTPStatus**: The return status of the model running in the background. If the mode has finished `HTTPStatus` will be 200 if successful, and 400 otherwise.
3. **nVars**: Total number of variables.
4. **nIntVars**: Number of integer variables.
5. **nNLVars**: Number of nonlinear variables.
6. **nCons**: Total number of constraints.
7. **nNLCons**: Number of nonlinear constraints.
8. **nNz**: Number of nonzero matrix elements.
9. **nIters**: Number of iterations.
10. **nBranches**: Number of branches (IPs only).
11. **sumInfeas**: Sum of infeasibilities.
12. **objVal**: Objective value.
13. **objBnd**: Objective bound (IPs only).
14. **objBest**: Best objective value found so far (IPs only).

## Logs

When a model is running it will write a `.log` file which will display output data and any errors. An effective way to diagnose a problem with your model is to view the log file. To do so, use the GET request on log:

```curl
curl --location --request GET 'http://localhost:8000/log/{MODEL_ID}'
```

This will display the log file in the terminal. Alternatively, you may type the URL `http://localhost:8000/log/{MODEL_ID}` in your browser and the file will download.

## chess.lng

As a refrence bellow is the `chess.lng` mentioned throughout the cURL samples.

```
MODEL:
SETS:
	NUTS: SUPPLY;
	BRANDS: PRICE, PRODUCE;
	NCROSSB( NUTS, BRANDS): FORMULA;
ENDSETS 

DATA:
	NUTS = @POINTER( 1);
	BRANDS = @POINTER( 2);
	SUPPLY = @POINTER( 3);
	PRICE = @POINTER( 4);
	FORMULA = @POINTER( 5);
ENDDATA 

MAX = @SUM( BRANDS( I): PRICE( I) * PRODUCE( I));
@FOR( NUTS( I): 
	@SUM( BRANDS( J): FORMULA( I, J) * PRODUCE( J) / 16) <= SUPPLY( I) );

DATA:

	@POINTER( 6) = PRODUCE;
	@POINTER( 7) = @STATUS();

ENDDATA
END

```

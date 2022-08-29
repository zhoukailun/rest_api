# Instructions

A REST API project based on fastapi

- language: Python
- framework: [fastapi](https://github.com/tiangolo/fastapi)
- backend db: [sqlite](https://github.com/sqlite/sqlite)
- sql toolkit: [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)

## Table of Contents

- [Download](#Download)
- [Deploy](#Deploy)
  - [Run with VirtualEnv](#Run-with-VirtualEnv)
  - [Run with Docker](#Run-with-Docker)
- [API Docs](#API-Docs)
  - [Create](#Create)
  - [Search by id](#Search-by-id)
  - [Search by query](#Search-by-query)
  - [Update](#Update)
  - [Tests](#Tests)
  - [Interactive API docs](#Interactive-API-docs)
  - [Alternative API docs](#Alternative-API-docs)
- [Project Structure](#Project-Structure)
- [Maintainers](#maintainers)


# Download

```sh
# download code to current directory
git clone https://github.com/zhoukailun/rest_api.git
```

# Deploy
## Run with VirtualEnv
VirtualEnv files was included in the package
```sh
# go to the project directory
$ cd ./rest_api

# activate virtualenv
$ source venv/bin/activate

# run service
$ uvicorn app.main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Run with Docker
Run service for the first time
```sh
# go to the project directory
$ cd ./rest_api

# build image from Dockerfile
$ docker build -f ./build/Dockerfile -t rest_api:latest .

# run container
$ docker run -d --name=rest_api_service -p 8000:8000  -v $PWD:/rest_api rest_api:latest
```
Manage service
```sh
# stop service
$ docker stop rest_api_service

# start service
$ docker start rest_api_service

# restart service
$ docker restart rest_api_service

# check logs within 100 lines
$ docker logs --tail=100  rest_api_service
```

Test service
```sh
# import 100 mock objects for testing
$ curl -X 'POST' 'http://127.0.0.1:8000/api/v1/tests/import?start=1&end=100'
```


# API Docs

## Create
- **API**: /api/v1/assets/update
- **Method**: POST
- **Description**: Create rack and pdu objects
- **Input body Example**:
```json
{
    "data": [
        {
            "asset_type": "pdu",
            "pdu_id": "pdu001",
            "pdu_capacity": 20.5,
            "pdu_outlets_number": 10
        },
        {
            "asset_type": "rack",
            "rack_id": "rack001",
            "rack_height": 1100,
            "rack_location": "SG-DC1-Suite1"
        }
    ]
}
```

| name  | type | required | default value | description |
| ----- | ---- | -------- | ------------- | ----------- |
| data  | **List** of pdu or rack object |yes|N/A|object list to create |

PDU object

| name  | type | required | default value | description |
| ----- | ---- | -------- | ------------- | ----------- |
| asset_type | **String** |yes|N/A|value: "pdu"|
| pdu_id | **String** |yes|N/A|pdu id|
| pdu_capacity | **Float** |no|0|pdu capacity, unit: kW|
| pdu_outlets_number | **Int** |no|0|pdu outlets total numbers|

Rack object

| name  | type | required | default value | description |
| ----- | ---- | -------- | ------------- | ----------- |
| asset_type | **String** |yes|N/A|value: "rack"|
| rack_id | **String** |yes|N/A|rack id|
| rack_height | **Float** |no|0|rack height, unit: mm|
| rack_location | **String** |no|""|rack location|

- **Response Type**: JSON
- **Successful Status Code**: 201
- **Response Example**:
```json
{
  "result": true,
  "count_succ": 2,
  "messages": "Create Data Successfully."
}
```

## Search by id
- **API**: /api/v1/assets/{asset_type}/search
- **Method**: GET
- **Description**: Search rack and pdu objects by rack_id or pdu_id
- **Input Parameters Example**:
```sh
$ curl 'http://127.0.0.1:8000/api/v1/assets/rack/search?asset_id=rack001'
$ curl 'http://127.0.0.1:8000/api/v1/assets/pdu/search?asset_id=pdu001'
```

| name  | type | required | default value | description |
| ----- | ---- | -------- | ------------- | ----------- |
| asset_type  | **String** |yes|N/A|enumerated values:  "rack", "pdu"|
| asset_id  | **String**  |yes|N/A|values of rack_id or pdu_id depends on the asset_type |

- **Response Type**: JSON
- **Successful Status Code**: 200
- **Response Example**:
```json
{
  "result": true,
  "count_succ": 1,
  "messages": "Search data successfully.",
  "data": [
    {
      "pdu_id": "pdu001",
      "pdu_capacity": 20.5,
      "pdu_outlets_number": 10,
      "create_time": "2022-08-29 04:43:51.434200",
      "update_time": "2022-08-29 04:43:51.434219"
    }
  ]
}
```

## Search by query
- **API**: /api/v1/assets/search
- **Method**: POST
- **Description**: Search rack and pdu objects by query conditions
- **Input body Example**:
```json
{
  "asset_type": "pdu",
  "fields_selected": [
    "pdu_id", "pdu_capacity"
  ],
  "condition": [
    {
      "field": "pdu_capacity",
      "operator": "ge",
      "value": 10
    }
  ]
}
```

| name  | type | required | default value | description |
| ----- | ---- | -------- | ------------- | ----------- |
| asset_type  | **String** |yes|N/A|enumerated values:  "rack", "pdu" |
| fields_selected  | **List** of object fields |no|[]|select fields to return, return all fields by default |
| condition  | **List** of conditions |no|[]| condition list to query |

condition object

| name  | type | required | default value | description |
| ----- | ---- | -------- | ------------- | ----------- |
| field | **String** |yes|N/A|object filed to filter|
| operator | **String** |yes|N/A|operator to filter the object field|
| value | **String/Int/Float** |yes|N/A|object field value to filter|

operator explain

| operator name  | explain | example |
| -------------- | ------- | ------- |
| eq | **==** |field "eq" "value"|
| ne | **!=** |field "ne" "value"|
| gt | **>** |field "gt" 0|
| lt | **<** |field "lt" 100|
| ge | **>=** |field "ge" 1|
| le | **<=** |field "le" 99|
| like | **like** |field "like" "%DC%"|
| regexp | **reguler expression** |field "regexp" "SG.*"|

- **Response Type**: JSON
- **Successful Status Code**: 200
- **Response Example**:
```json
{
  "result": true,
  "count_succ": 1,
  "messages": "Search data successfully.",
  "data": [
    {
      "pdu_id": "pdu001",
      "pdu_capacity": 20.5
    }
  ]
}
```

## Update
- **API**: /api/v1/assets/update
- **Method**: PUT
- **Description**: Update rack and pdu objects
- **Input body Example**:
```json
{
    "data": [
        {
            "asset_type": "pdu",
            "pdu_id": "pdu001",
            "pdu_capacity": 40.5,
            "pdu_outlets_number": 16
        },
        {
            "asset_type": "rack",
            "rack_id": "rack001",
            "rack_height": 1500,
            "rack_location": "SG-DC2-Suite2"
        }
    ]
}
```
Input body parameters are the same as [Create](#Create)

- **Response Type**: JSON
- **Successful Status Code**: 201
- **Response Example**:
```json
{
  "result": true,
  "count_succ": 2,
  "messages": "Update data successfully."
}
```

## Tests

- **API**: /api/v1/tests/import
- **Method**: POST
- **Description**: Import mock objects data for testing
- **Input Parameters Example**:
```sh
$ curl -X 'POST' 'http://127.0.0.1:8000/api/v1/tests/import?start=1&end=100'
```

| name  | type | required | default value | description |
| ----- | ---- | -------- | ------------- | ----------- |
| start  | **Int** |no|1|test data start number|
| end  | **Int**  |no|100|test data end number |

- **Response Type**: JSON
- **Successful Status Code**: 201
- **Response Example**:
```json
{
  "result": true,
  "count_succ": 99,
  "messages": "Mock data 1-100 imported."
}
```

## Interactive API docs
After service is running, go to http://127.0.0.1:8000/docs
You will see the automatic interactive API documentation (provided by [Swagger](https://github.com/swagger-api/swagger-ui) UI):

- The interactive API documentation will be automatically updated, including the new body:
- Click on the button "Try it out", it allows you to fill the parameters and directly interact with the API:
- Then click on the "Execute" button, the user interface will communicate with your API, send the parameters, get the results and show them on the screen:

## Alternative API docs
Also, go to http://127.0.0.1:8000/redoc
You will see the alternative automatic documentation (provided by [ReDoc](https://github.com/Rebilly/ReDoc)):

# Project Structure

```.
├── README.md
├── app
│   ├── api
│   │   ├── response
│   │   │   └── sqlalchemy_response.py
│   │   └── routers
│   │       ├── api.py
│   │       ├── assets.py
│   │       └── default.py
│   ├── db
│   │   ├── database.py
│   │   ├── operators.py
│   │   └── tables.py
│   ├── main.py
│   └── models
│       ├── assets.py
│       ├── pdu.py
│       └── racks.py
├── build
│   └── Dockerfile
├── config.py
├── requirements.txt
├── tests
│   └── import_test_data.py
└── venv
```

## Maintainers

[@Zhou Kailun](https://github.com/zhoukailun).


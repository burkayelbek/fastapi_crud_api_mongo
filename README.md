# FastAPI_Case

## Requirements in the App

* Python 3.10
* MongoDB
* .env file in the project

## Description
This project is built with FastAPI framework for doing CRUD operations

## Installation

#### Example .env file content:
* MONGODB_DB=db_name
* MONGODB_HOST=db_hosst
* MONGODB_USER=db_user
* MONGODB_PASSWORD=db_password
* MONGODB_PORT=db_port

And after that

```shell
$ virtualenv -p python3 venv
$ Activate virtualenv:
$ - WINDOWS: .\venv\Scripts\activate
$ - LINUX: source venv\bin\activate
$ pip install -r requirements.txt
$ cp .env.example .env
$ uvicorn main:app --reload
```
# Hotels Nearby

This Project serve as a geolocation service to find Hotels Nearby 

### Table of Contents

-   [Getting Started][1]
    -   [Prerequesites][2]
    -   [How to Run Backend Server][3]
    -   [Run Unit Testing][3]
-   [Usage][4]
    -   [Authentication Token][5]

## Getting Started

The project involves a backend api which contains functionality to retrieve information about nearby Hotels base on some coordinates. 
it will use sqlite to store it locally on the database and the docs are automate created using swagger

### Prerequisites

Activate the virtual environment
Install the the require packages via pip 

```
python3 -m venv env
source env/bin/activate
pip3 install -U -r requirements.txt
```


### Running

On the root folder run 

```
flask run
```

### Run Unit Testing

```
python -m pytest -s tests/test_api.py
```

## Usage

You have to generate a token for authentication with the backend api running this commands sending 
username as a parameter

```
flask generate_admin_jwt username
```

## 
Usage
Both install options expose the backend on [http://127.0.0.1:5000]
(http://127.0.0.1:5000), with docs at [http://127.0.0.1:8000/docs])

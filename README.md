# Backend - Shamba API 
Shamba App is an app to be used to manage the activities in the farm so as to monitor the various steps in farming, It involves tracking the procedures to be done, all inputs such as fertilizer, the field it was done on( if a farm has different fields) and the worker who worked on it. 

# API URL
Heroku: [https://shamba.herokuapp.com/]
Localhost: base URL is localhost:5000

[Login](https://maureen-fsnd.us.auth0.com/authorize?audience=farm&response_type=token&client_id=aiUv8rPCDbI4u59awC0Qy7Tv8wxVJjuN&redirect_uri=https://127.0.0.1:5000/login)

# Authentication
The tokens are provided in the setup.sh file and are valid for 24hours. A postman collectiom is also included within the project.

# User Roles
## Manager
Can do all CRUD activites, e.g create farm procedures, create inputs. delete etc

## Farm manager
Does the bulk of the farm management activities except deleting any data. The Farm manager can add, update and view all records.


### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, create a database using the setup.psql file provided. From the backend/backend folder, in terminal run:
```bash
   psql postgres < setup.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Endpoints 
#### GET /procedures
- General:
    - Returns a list of procedure objects, success value, and total number of procedures
    
- Sample: `curl http://127.0.0.1:5000/procedures`

``` 
{
    "procedures": [
        {
            "activity": "Fertilizer application",
            "date": "Wed, 10 Feb 2021 00:00:00 GMT",
            "field": "Field 1",
            "id": 3,
            "image_link": "https://imagelink.com",
            "input": "ABC Fertilizer",
            "inputs_qty": 10,
            "name": "Name 1",
            "worker": "Test Worker"
        }
    ],
    "success": true,
    "total_procedures": 1
}
```

#### POST /procedures
- General:
    - Creates a new procedure using the submitted values i.e., answer, difficulty, category and rating. 
    - Returns the id of the created question, success value, total question, and questions list based on current page number to update the frontend. 
     
- `curl http://127.0.0.1:5000/questions?page=1 -X POST -H "Content-Type: application/json" -d '{"name":"Procedure", "date":"2021-07-28", "activity":"Fertilizer application","field_id":2, "worker_id":1,"input_id":1,"inputs_quantity":10,"image_link":"https://imagelink.com"}'`
```
{
    "created": 4,
    "procedure": {
        "activity": "Fertilizer application",
        "date": "Wed, 28 Jul 2021 00:00:00 GMT",
        "field": 2,
        "id": 4,
        "image_link": "https://imagelink.com",
        "input": 1,
        "inputs_qty": 10,
        "name": "Procedure 1",
        "worker": 1
    },
    "success": true
}
```
#### DELETE /procedures/{procedure_id}
- General:
    - Deletes the procedures of the given ID if it exists. Returns the success value and the id of the deleted value
- `curl -X DELETE http://127.0.0.1:5000/procedures/4`
```
{
    "delete": "4",
    "success": true
}
```

#### PATCH /procedures/{procedure_id}
- General:
    - Update the data in the procedures of the given ID if it exists. Returns the success value
- `curl http://127.0.0.1:5000/procedures/3  -X PATCH -H "Content-Type:application/json" -d '{"name":"First Input Application"}'`
{
    "procedure": [
        {
            "activity": "Fertilizer application",
            "date": "Wed, 10 Feb 2021 00:00:00 GMT",
            "field": 2,
            "id": 3,
            "image_link": "https://imagelink.com",
            "input": 1,
            "inputs_qty": 10,
            "name": "First Input Application",
            "worker": 1
        }
    ],
    "success": true
}


#### GET /inputs/
- General:
    - Returns a list of input objects, success value, and total number of inputs
  
- Sample: `curl http://127.0.0.1:5000/inputs/1/`

```{
    "inputs": [
        {
            "id": 1,
            "metrics": "Kg",
            "name": "ABC Fertilizer",
            "quantity": 10
        }
    ],
    "success": true
}
```


#### POST /inputs
- General:
    -  Gets inputs to be applied to the farm. 
  
    - Returns one inputs details and a success value
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[13,15],"quiz_category":{"type":"Science","id":"1"}}'`

```{
    "inputs": {
        "id": 2,
        "metrics": "Kg",
        "name": "CBDE Fertilizer",
        "quantity": 30
    },
    "success": true
}
```


#### DELETE  /inputs/{input_id}
- General:
    - Deletes the input of the given ID if it exists. Returns the success value and the id of the deleted value
- `curl -X DELETE http://127.0.0.1:5000/inputs/2`
```
{
    "delete": "2",
    "success": true
}
```

#### PATCH /inputs/{input_id}
- General:
    - Update the data in the input of the given ID if it exists. Returns the success value
- `curl http://127.0.0.1:5000/inputs/1  -X PATCH -H "Content-Type:application/json" -d '{ "name": "DFG Fertilizer"}'`
```
{
    "inputs": [
        {
            "id": 1,
            "metrics": "Kg",
            "name": "DFG Fertilizer",
            "quantity": 10
        }
    ],
    "success": true
}
```



#### POST /fields
- General:
    - Creates a new field using the submitted type. 
    - Returns the id of the created field, success value, total number of field, and field data created.
- `curl http://127.0.0.1:5000/fields -X POST -H "Content-Type: application/json" -d '{"name":"Field 5", "size":2.3}'`
   
```
{
    "fields": {
        "id": 4,
        "name": "Field 5",
        "size": 1.4
    },
    "success": true
}

```

#### GET /fields/
- General:
    - Returns a list of field objects, success value, and total number of fields

- Sample Request: `curl http://127.0.0.1:5000/fields/`

- Sample Response

```{
    "fields": [
        {
            "id": 2,
            "name": "Field 1",
            "size": 1.9
        },
        {
            "id": 3,
            "name": "Field 1",
            "size": 1.1
        },
        {
            "id": 4,
            "name": "Field 5",
            "size": 1.4
        }
    ],
    "success": true
}
```



#### PATCH /fields/{field_id}
- General:
    - Update the data in the field of the given ID if it exists. Returns the success value
- `curl http://127.0.0.1:5000/field/2  -X PATCH -H "Content-Type:application/json" -d '{ "size": 5.6}'`
```
{
    "field": [
        {
            "id": 2,
            "name": "Field 1",
            "size": 5.6
        }
    ],
    "success": true
}
```

#### DELETE  /fields/{field_id}
- General:
    - Deletes the field of the given ID if it exists. Returns the success value and the id of the deleted value
- `curl -X DELETE http://127.0.0.1:5000/field/4`
```
{
    "delete": "4",
    "success": true
}
```


#### POST /workers
- General:
    - Creates a new worker using the submitted data. 
    - Returns the id of the created worker, success value, total number of workers, and worker data created.
- Sample Request `curl http://127.0.0.1:5000/fields -X POST -H "Content-Type: application/json" -d '{"name": "Test User","national_id":785784754,"phone_number":"+254637658475","type": "Casual"}'`
   
```
{
  "name": "Test User",
  "national_id":785784754,
  "phone_number":"+254637658475",
  "type": "Casual"
}

```

#### GET /workers/
- General:
    - Returns a list of worker objects, success value, and total number of workers
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample Request: `curl http://127.0.0.1:5000/workers/`

- Sample Response: 

```{
    "success": true,
    "workers": [
        {
            "id": 1,
            "name": "Maureen Mumbi",
            "national_id": null,
            "phone_number": null,
            "type": "Casual"
        },
        {
            "id": 2,
            "name": "Maureen Maina",
            "national_id": 785784754,
            "phone_number": "+254637658475",
            "type": "Casual"
        },
        {
            "id": 3,
            "name": "Test User ",
            "national_id": 785784754,
            "phone_number": "+254637658475",
            "type": "Casual"
        }
    ]
}
```



#### PATCH /workers/{worker_id}
- General:
    - Update the data in the field of the given ID if it exists. Returns the success value
- `curl http://127.0.0.1:5000/workers/1  -X PATCH -H "Content-Type:application/json" -d '{ "national_id": 5648790, "phone_number":"+2546236276373"}'`
```
{ 
    "national_id": 5648790, 
    "phone_number":"+2546236276373"
}
```

#### DELETE  /workers/{worker_id}
- General:
    - Deletes the worker of the given ID if it exists. Returns the success value and the id of the deleted value
- `curl -X DELETE http://127.0.0.1:5000/workers/3`
```
{
    "delete": "3",
    "success": true
}
```


## Testing
To run the tests, run
```
dropdb shamba_test
createdb shamba_test
psql shamba_test < test_shamba.psql
python test_shamba.py
```


## Errors 
For errors, the server returns a json object with a description of the type of error. Find the description below:

# 400 (Bad Request)
  {
    "success": False, 
    "error": 400,
    "message": "bad request, please check your input"
  }

# 401 (Unauthorised)
  {
    "success": False, 
    "error": 401,
    "message": "authorisation error(will be different depending on whwther permission is not found or token is expired"
  }

# 403 (Forbiddden request)
  {
    "success": False, 
    "error": 403,
    "message": "Permission not found"
  }

# 404 (Resource Not Found)
  {
    "success": False, 
    "error": 404,
    "message": "resource not found"
  }

# 405 (Method not allowed)
  {
    "success": False, 
    "error": 405,
    "message": "Method not allowed"
  }

# 422 (Unprocessable entity)
  {
    "success": False, 
    "error": 422,
    "message": "unprocessable"
  }

# 500 (Internal server error)
  {
    "success": False, 
    "error": 500,
    "message": "Server error
  }

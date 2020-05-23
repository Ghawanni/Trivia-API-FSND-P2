# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


# API Reference

----

- Base URL: currently, this backend only runs locally at port 5000. So kindly use *127.0.0.1:5000* to connect to end points for this backend
- This application does not require any **authentication**, you're good to go

## Error Handling

Errors returned from this backend are all returned in the following format:
```
{
  'success': False,
  'error': 404,
  'message': 'resource not found'
}
```

There are 3 possible error responses the API could return, here's each possible response and it's meaning:

- *400*: Bad Request
- *404*: Not Found
- *422*: Cannot Proccess Request


## Endpoints

### **GET /categories**
- returns all categories in the database
- the indecies start from 1
- sample request `curl localhost:5000/categories`
```JSON
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### **GET /questions**

- returns all questions in the system
- questions are paginated 10/page
- can accept *page* query string to specify page number
- Sample `curl localhost:5000/questions`
```JSON
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
.
.
.
  ],
  "success": true,
  "total_questions": 19
}
```



### **DELETE /questions/<int:questionId>**

- deletes a question based on the question id
- sample `curl localhost:5000/questions/4`
```JSON
{
  "success": true
}
```


### **POST /questions**
- can have two modes
  - create questions
    - requires body with the following attributes
      - question (string)
      - answer (string)
      - category (integer)
      - difficulty (integer)
    - example: `curl -H "Content-Type: application json" -X POST --data '{"question": "What international movie won an Oscar in 2020", "answer": "Parasite", "category": 5, "difficulty": 2}' localhost:5000/questions`
```JSON
  {
  "question": {
    "answer": "Parasite",
    "category": 5,
    "difficulty": 2,
    "id": 24,
    "question": "What international movie won an Oscar in 2020"
  },
  "success": true
  }
```
- You can also search based on a search term which is passed as query parameter `curl -X POST localhost:5000?term=movie`
- this will return all questions with the word "**movie**" in the following format:
  
```JSON
{
  "current_category": "",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```


### **GET /categories/<int:categoryId>/questions**
- this endpoint will get questions in a specific category only
- the category id is passed in the url path (an integer)
- sample `curl localhost:5000/categories/4/questions`
```JSON
{
  "current_category": {
    "id": 4,
    "type": "History"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

### **POST /quizzes**
- this endpoint will return a a question to be displayed based on parameters sent in the body
- this body to this endpoint should contain the follownig:
  - _quiz_category[integer]_ : this JSON object should contain an attribute id which will identify which category we want to get questions from. **pass 0 for all categories**
  - _previous_questions[integer array]_ : this array is supposed to include integers for question ids that are already displayed to the user. So that none of those questions is returned again in the same quiz
- sample: 
`curl -H "Content-Type: application/json" -X POST --data '{ "quiz_category": {"id":0},  "previous_questions": [2,4,8] }' localhost:5000/quizzes`

```JSON
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```
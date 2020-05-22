import os
import json
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func, not_
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app,resources={r"*": {"origins": "*"}})


  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''


  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", 'Content-Type,Authorization,true')
    return response


  '''
  helper function to paginate questions
  '''
  def paginate_questions(request, selection):
    page_num = request.args.get('page', 1, type=int)
    start = (page_num - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in selection]
    paginated_books = formatted_questions[start:end]

    return paginated_books


  '''
  @DONE:
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=["GET"])
  def get_all_categories():

    categories = Category.query.order_by(Category.id).all()
    categories_dict = {}

    for category in categories:
      categories_dict[category.id] = category.type

    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories_dict
    })


  '''
  @DONE:: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=["GET"])
  def get_questions():

    all_questions = Question.query.order_by(Question.id).all()
    paginated_questions = paginate_questions(request, all_questions)

    # same logic to get all categories
    categories = Category.query.order_by(Category.id).all()
    categories_dict = {}

    # create a dictionary<key=categoryId>: <value=categoryType>
    for category in categories:
      categories_dict[category.id] = category.type

    if len(paginated_questions) == 0 or len(categories_dict) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': paginated_questions,
      'total_questions': len(Question.query.all()),
      'current_category': "", # no need to return current category if we're viewing all questions
      'categories': categories_dict
    })

  '''
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: W'hen you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:questionId>', methods=["DELETE"])
  def delete_question(questionId):

    question = Question.query.filter(Question.id == questionId).one_or_none()
    
    if question is None:
      abort(422)

    Question.delete(question)

    return jsonify({
      'success': True
    })

  '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=["POST"])
  def create_new_question():
    error = False

    # if we're searching for a term 
    if request.args:
      search_term = (request.args['term'])
      search_result = Question.query.filter(func.lower(Question.question).contains(search_term.lower())).all()
      
      if len(search_result) == 0:
        abort(422)
      else:
        formatted_questions = [question.format() for question in search_result]
        return jsonify({
          'success': True,
          'questions': formatted_questions,
          'total_questions': len(Question.query.all()),
          'current_category': ""
        })

    # if we're submitting a new question
    elif not request.args:
      try:
        question_to_add = Question( question = request.json['question'],
                                    answer = request.json['answer'], 
                                    category=request.json['category'], 
                                    difficulty=request.json['difficulty'])
        Question.insert(question_to_add)
      except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
      finally:
        if error:
          abort(422)
        else:
          return jsonify({
            'success': True,
            'question': question_to_add.format()
          })

  '''
  @DONE:: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @DONE:
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:categoryId>/questions', methods=["GET"])
  def get_questions_by_category(categoryId):
    questions_by_category = Question.query.filter(Question.category==categoryId).all()
    formatted_questions = [question.format() for question in questions_by_category]
    current_category = Category.query.get(categoryId)
    if(len(questions_by_category) == 0):
      abort(404)
    else:
      return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(Question.query.all()),
        'current_category': current_category.format()
      })
  '''
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=["POST"])
  def start_quiz():
    quiz_category = request.json['quiz_category']
    previous_questions = request.json['previous_questions'] # frontend will send ids of previous questions
    possible_questions = []

    # handle case for all categories
    if quiz_category['id'] == 0:
      possible_questions = Question.query.filter(not_(Question.id.in_(previous_questions))).all()
    elif int(quiz_category['id']) > 0:
      category_id = int(quiz_category['id'])
      possible_questions = Question.query.filter(Question.category == category_id).\
                                          filter(not_(Question.id.in_(previous_questions))).all()


    if len(possible_questions) == 0:
      abort(422)
    else:
      formatted_questions = [question.format() for question in possible_questions]
      return jsonify({
        'success': True,
        'question': random.choice(formatted_questions)
      })
    

  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'cannot process request'
    }), 422

  
  return app

    
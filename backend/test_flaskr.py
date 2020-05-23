import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Why did the chcken cross the road?',
            'answer': 'To get to the other side',
            'category': 1,
            'difficulty': 5
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE:
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
    def test_get_question_failed(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)


    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    def test_create_question_failed(self):
        res = self.client().post('/questions',\
             json={'not_correct_params': False})
        data = json.loads(res.data)

        self.assertEqual(data['error'], 422)
        self.assertEqual(data['success'], False)


    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    def test_delete_question_failed(self):
        res = self.client().delete('/questions/2001')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    

    def test_search_term(self):
        res = self.client().post('/questions?term=who')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertTrue(data['total_questions'])
    def test_search_term_failed(self):
        res = self.client().post('/questions?term=owiefjewofij')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    def test_get_questions_by_category_failed(self):
        res = self.client().get('/categories/11/questions', \
            json={'something_wrong': 'I shouldn\'t be here'})
        data  = json.loads(res.data)
        
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)

    
    def test_start_quiz(self):
        res = self.client().post('quizzes',\
            json={'quiz_category': {'id': 3},
            'previous_questions': [4,2,8]})
        data = json.loads(res.data)
        previous_questions = [4,2,8]

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['id'] not in previous_questions)
    def test_start_quiz_all_categories(self):
        res = self.client().post('quizzes',\
            json={'quiz_category': {'id': 0},
            'previous_questions': [4,2,8]})
        data = json.loads(res.data)
        previous_questions = [4,2,8]

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['id'] not in previous_questions)
    def test_start_quiz_failed(self):
        res = self.client().post('quizzes',\
            json={'quiz_category': {'id': 12},
            'previous_questions': []})
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
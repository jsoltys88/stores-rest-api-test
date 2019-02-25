"""
Base Test

This should be the parent class to each non-unit test/
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.

"""

from unittest import TestCase
from app import app
from db import db

class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # runs once for the whole class (so for each method in the class as a whole)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['DEBUG'] = False
        app.config['PROPAGATE EXCEPTIONS'] = True
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        # Make sure database exists - we will create a new db
        # this runs once for each method in the class

        with app.app_context():
            db.create_all()

        # Get a test client
        self.app = app.test_client()
        self.app_context = app.app_context # it allows to access app_context later on in our test

    def tearDown(self):
        # Make sure database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()

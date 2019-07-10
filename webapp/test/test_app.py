import app
import os
import tempfile
import unittest


class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        with app.app.app_context():
            app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

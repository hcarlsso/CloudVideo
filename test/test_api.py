import flask
import unittest
import json
import uuid

from faafo.api import create_app

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):

        options = {
            'config_dict' : {
                'DEBUG' : True,
                'SQLALCHEMY_DATABASE_URI' : 'sqlite:////tmp/sqlite.db'
            }
        }
        self.app = create_app(**options)

    def test_simple(self):
        with self.app.test_client() as c:
            resp = c.get('/')
            self.assertEqual(resp.status_code, 202)


    def test_check_queue(self):
        with self.app.test_client() as c:
            my_uuid = str(uuid.uuid4())
            resp = c.get('/queue/' + my_uuid)
            self.assertEqual(resp.status_code, 404)



if __name__ == '__main__':
    unittest.main()

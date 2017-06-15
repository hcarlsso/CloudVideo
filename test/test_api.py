import flask
import unittest
import json
import uuid

from faafo.api.service import app

class FlaskrTestCase(unittest.TestCase):

    def test_simple(self):
        with app.test_client() as c:
            resp = c.get('/')
            self.assertEqual(resp.status_code, 202)


    def test_check_queue(self):
        with app.test_client() as c:
            my_uuid = str(uuid.uuid4())
            resp = c.get('/queue/' + my_uuid)
            self.assertEqual(resp.status_code, 404)



if __name__ == '__main__':
    unittest.main()

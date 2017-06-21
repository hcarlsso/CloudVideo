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
                'SQLALCHEMY_DATABASE_URI' : 'sqlite:////tmp/sqlite.db',
                'TESTING' : True,
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

    def test_post_db(self):
        with self.app.test_client() as c:
            my_uuid = str(uuid.uuid4())
            res = {
                'uuid' : my_uuid,
                'url' : 'bajs',
                'status' : 1
            }
            import pdb; pdb.set_trace()
            resp = c.put('/v1/queue/' + my_uuid)

            # Write more here on the put method


if __name__ == '__main__':
    unittest.main()

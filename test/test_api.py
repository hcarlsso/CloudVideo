import flask
import unittest
import json
import uuid
import os
import tempfile

from faafo.api import create_app

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):

        self.db_fd , self.filepath_db = tempfile.mkstemp()

        options = {
            'config_dict' : {
                'DEBUG' : True,
                'SQLALCHEMY_DATABASE_URI' : 'sqlite:///' + self.filepath_db,
                'TESTING' : True,
                'SQLALCHEMY_TRACK_MODIFICATIONS' : False
            }
        }
        self.app = create_app(**options)

    def tearDown(self):

        if os.path.isfile(self.filepath_db):
            os.close(self.db_fd)
            os.unlink(self.filepath_db)

    def test_simple(self):
        with self.app.test_client() as c:
            resp = c.get('/')
            self.assertEqual(resp.status_code, 202)


    def test_check_queue(self):
        with self.app.test_client() as client:
            my_uuid = str(uuid.uuid4())
            resp = client.get('/queue/' + my_uuid)
            self.assertEqual(resp.status_code, 404)

    def test_post_db(self):
        with self.app.test_client() as client:
            my_uuid = str(uuid.uuid4())
            ref = {
                'uuid' : my_uuid,
                'url' : 'bajs',
                'status' : 1
            }
            headers = {'content-type': 'application/json'}
            resp_post = client.post('/v1/queue' , data= json.dumps(ref),
                               headers = headers)
            self.assertEqual(resp_post.status_code, 201)


            resp_get = client.get('/v1/queue/' + my_uuid)
            self.assertEqual(resp_get.status_code, 200)
            self.assertDictEqual(json.loads(resp_get.data), ref)


if __name__ == '__main__':
    unittest.main()

import flask
import unittest
import json

import sys
# import pdb; pdb.set_trace()
from faafo.api.service import app

class FlaskrTestCase(unittest.TestCase):

    def test_simple(self):
        with app.test_client() as c:
            resp = c.get('/')
            self.assertEqual(resp.status_code, 202)





if __name__ == '__main__':
    unittest.main()

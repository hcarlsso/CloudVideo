# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys

from pprint import pprint
pprint(sys.path)

import httpretty
from sure import expect
import unittest
import sys

from faafo import client

class TestRest(unittest.TestCase):
    @httpretty.activate
    def test_rest(self):
        url = "http://localhost:8090/"
        httpretty.register_uri(httpretty.GET, url,
                               body='{"status": "ok"}',
                               content_type="application/json")


        response = client.make_one_request(url)
        expect(response.json()).to.equal({"status": "ok"})

if __name__ == '__main__':
    unittest.main()

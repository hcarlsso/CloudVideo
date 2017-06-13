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

import httpretty
from sure import expect
import unittest
import sys

from faafo import client

class TestRest(unittest.TestCase):
    @httpretty.activate
    def test_rest(self):
        url = "http://localhost:8090/"
        queue_location = "queue/12345"
        body = '{"location": "%s"}' % queue_location
        # import pdb; pdb.set_trace()
        httpretty.register_uri(
            httpretty.GET, url,
            body=body,
            status = 202,
            content_type="application/json"
        )

        # Responses in the queue
        # Can include more information here
        responses=[
            httpretty.Response(
                body='{"status": "pending"}',
                status=200,
                content_type="application/json",
            ),
            httpretty.Response(
                body='{"status": "ready"}',
                status=303,
                content_type="application/json",
            ),
        ]
        httpretty.register_uri(
            httpretty.GET, url +  queue_location,
            responses = responses
        )

        response = client.make_one_request(url)
        # expect(response.json()).to.equal({"status": "ok"})

    @httpretty.activate
    def test_wait(self):
        url = "http://localhost:8090/"
        queue_location = "queue/12345"

        # Responses in the queue
        # Can include more information here
        responses=[
            httpretty.Response(
                body='{"status": "pending"}',
                status=200,
                content_type="application/json",
            ),
            httpretty.Response(
                body='{"status": "ready"}',
                status=303,
                content_type="application/json",
            ),
        ]
        httpretty.register_uri(
            httpretty.GET, url +  queue_location,
            responses = responses
        )
        data  = client.wait_to_transfer(url + queue_location)
        self.assertDictEqual(data, {'status':'ready'})

if __name__ == '__main__':
    unittest.main()

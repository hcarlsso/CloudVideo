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
import tempfile
import os

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

        # Create the file to stream
        f = tempfile.NamedTemporaryFile(delete=False)
        path = f.name
        f.write("Hello World!\n")
        f.close()
        print(path)
        response = client.make_one_request(url, path)
        # expect(response.json()).to.equal({"status": "ok"})

        os.unlink(path)

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


    @httpretty.activate
    def test_upload(self):
        url = "http://localhost:8090/queue/12345"
        body = '{"status": "uploading"}'
        httpretty.register_uri(
            httpretty.POST, url,
            status = 200,
            body=body,
            content_type="application/json"
        )

        # Create the file to stream
        f = tempfile.NamedTemporaryFile(delete=False)
        path = f.name
        f.write("Hello World!\n")
        f.close()

        response = client.send_file(url, path)

        expect(response.text).to.equal(body)
        expect(httpretty.last_request().method).to.equal("POST")

        # How to test that we got the right answer?

        os.unlink(path)


if __name__ == '__main__':
    unittest.main()

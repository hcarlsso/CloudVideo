import unittest
import tempfile
import os
import hashlib
import httpretty
import uuid
import kombu

from faafo.worker.service import VideoConverter
from faafo.worker.service import Worker

class TestVideoConversion(unittest.TestCase):

    def test_simple(self):

        fd_output, filepath_output = tempfile.mkstemp()
        path = os.path.dirname(__file__)

        path_input_video = os.sep.join([path, 'SampleVideo_1280x720_1mb.mkv'])

        obj = VideoConverter(path_input_video, filepath_output)

        ref_sum = '23dd5b552d16b53de705e1762965da9a2a843427aec147aa1d22f48face6d88a'
        out_sum = hashlib.sha256(open(filepath_output, 'rb').read()).hexdigest()

        self.assertEqual(out_sum, ref_sum)

        os.close(fd_output)
        os.unlink(filepath_output)

class TestWorker(unittest.TestCase):
    @httpretty.activate
    def test_prepare_for_job(self):


        my_uuid = str(uuid.uuid4())

        base_url = "http://localhost:8090"
        url = base_url + "/v1/queue/" + my_uuid
        httpretty.register_uri(
            httpretty.PUT,
            url,
            body='{}',
            status = 200,
            content_type="application/json"
        )
        task = {
            'uuid' : my_uuid
        }

        conn = kombu.Connection("memory://")
        queue = conn.SimpleQueue('myqueue')
        queue.put('test')
        msg = queue.get(timeout=1)

        worker = Worker(conn, queue, base_url)

        res = worker.process(task, msg)

        self.assertDictEqual(
            res,
            {
                'uuid' : my_uuid,
                'status' : 2,
                'url' : 'localhost'
            }
        )


if __name__ == '__main__':
    unittest.main()

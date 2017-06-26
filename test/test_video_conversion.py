import unittest
import tempfile
import os
import hashlib
from faafo.worker.service import VideoConverter


class TestRest(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()

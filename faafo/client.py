#!/usr/bin/env python

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

import requests
from pprint import pprint
import time
import shutil
MAX_WAIT_CYCLES = 10
WAIT_BETWEEN_CYCLES = 0.1
OUTPUTFILE = "output.avi"

def wait_to_transfer(url):
    '''
    How to ensure we dont wait until infinity
    '''

    wait_to_transfer = True
    cycles = 0
    while wait_to_transfer or cycles < MAX_WAIT_CYCLES:
        response = requests.get(url)
        if response.status_code == 200:
            wait_to_transfer = False
            time.sleep(WAIT_BETWEEN_CYCLES)
        elif response.status_code == 303:
            pass
        else:
            raise StandardError

        cycles = cycles + 1

    return response.json()

def send_file(url, file_to_send):

    return requests.post(url, files={'file': open(file_to_send, 'rb')})

def make_one_request(url, file_to_send):

    # s = requests.session()

    session = requests.session()
    response = session.get(url)

    # Accepted
    if response.status_code == 202:
        # We are safe to
        data = response.json()

        if 'location' in data:
            url_status = url + data['location']
            data = wait_to_transfer(url_status )
        else:
            raise StandardError

        # Upload the file
        resp_upload = send_file(url_status, file_to_send)
        info_upload = resp_upload.json()
        url_wait_conversion = url + info_upload['download_wait']

        # Wait for the file to be processed
        data = wait_to_transfer(url_wait_conversion)
        url_download = url + data['download']

        response_converted_video = session.get(url_download, stream = True)
        with open(OUTPUTFILE, "wb") as handle:
            shutil.copyfileobj(response_converted_video.raw, handle)
        # And we are done
    else:
        data = None

    return OUTPUTFILE

def main():
    pass

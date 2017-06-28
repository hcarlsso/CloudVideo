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

# based on http://code.activestate.com/recipes/577120-julia-fractals/

import base64
import copy
import hashlib
import json
import os
import random
import tempfile
import time
import socket

import subprocess as subp
import shlex

from kombu.mixins import ConsumerMixin
import requests


endpoint_url = 'TEMP'

class VideoConverter(object):

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.convert()

    def convert(self):

        cmd = """mencoder %s -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=3000
             -oac pcm -o %s""" % (self.source, self.destination)
        print('Convert command')
        print(cmd)
        print("Converting video file")
        subp.call(shlex.split(cmd))



class Worker(ConsumerMixin):
    '''
    Tell the queue worker is ready to work
    '''

    def __init__(self, connection, task_queue, endpoint):
        self.connection = connection
        self.endpoint = endpoint
        self.task_queue = task_queue

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.task_queue,
                         accept=['json'],
                         callbacks=[self.process])]

    def process(self, task, message):


        result = {
            'uuid': task['uuid'],
            'url': socket.gethostname(),
            'status' : 2, # Ready
        }

        # NOTE(berendt): only necessary when using requests < 2.4.2
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}

        requests.put(
            "%s/v1/queue/%s" % (self.endpoint, str(task['uuid'])),
            json.dumps(result), headers=headers)

        message.ack()
        return result

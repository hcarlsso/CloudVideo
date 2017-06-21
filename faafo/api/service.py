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

import uuid

import flask
from flask import jsonify
from kombu import Connection
from kombu.pools import producers
from sqlalchemy.dialects import mysql

from faafo import queues
from faafo import version


mainPage = flask.Blueprint('index',__name__)

@mainPage.route('/', methods=['GET'])
def index():
    # Create random string for identification
    my_uuid = str(uuid.uuid4())
    data = {'location' : 'queue/' + my_uuid}

    # Put the job inside the rabbit queue.
    return jsonify(data), 202


@mainPage.route('/queue/<string:jobid>', methods=['GET'])
def check_worker_queue(jobid):
    # Check in database for job.
    if True:
        # Job does not exists
        response = flask.jsonify({'code': 404,
                                  'status': 'job not found'})
        response.status_code = 404
    elif False:
        # Job is not ready to be processed
        response = flask.jsonify({'code': 200,
                                  'status': 'pending'})
        response.status_code = 200
    else:
        # Here the job is ready to be processed.
        response = flask.jsonify({'code': 303,
                                  'status': 'pending'})
        response.status_code = 303

    return response


def generate_fractal(**kwargs):
    with producers[connection].acquire(block=True) as producer:
        producer.publish(kwargs['result'],
                         serializer='json',
                         exchange=queues.task_exchange,
                         declare=[queues.task_exchange],
                         routing_key='normal')

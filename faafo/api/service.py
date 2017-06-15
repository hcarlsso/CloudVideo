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

import base64
import copy
import cStringIO
from pkg_resources import resource_filename
import uuid

import flask
import flask.ext.restless
import flask.ext.sqlalchemy

from flask import jsonify
from flask_bootstrap import Bootstrap
from kombu import Connection
from kombu.pools import producers
from oslo_config import cfg
from oslo_log import log
from PIL import Image
from sqlalchemy.dialects import mysql

from faafo import queues
from faafo import version

# LOG = log.getLogger('faafo.api')
# CONF = cfg.CONF

# api_opts = [
#     cfg.StrOpt('listen-address',
#                default='0.0.0.0', # If you have the debugger disabled or trust the users on your network, you can make the server publicly by listning on 0.0.0.0
#                help='Listen address.'),
#     cfg.IntOpt('bind-port',
#                default='80',
#                help='Bind port.'),
#     cfg.StrOpt('database-url',
#                default='sqlite:////tmp/sqlite.db',
#                help='Database connection URL.')
# ]

# CONF.register_opts(api_opts)

# log.register_options(CONF)
# log.set_defaults()

# CONF(project='api', prog='faafo-api',
#      default_config_files=['/etc/faafo/faafo.conf'],
#      version=version.version_info.version_string())

# log.setup(CONF, 'api',
#           version=version.version_info.version_string())

template_path = resource_filename(__name__, "templates")

# Create the Flask app
app = flask.Flask('faafo.api', template_folder=template_path)
# app.config['DEBUG'] = CONF.debug
# app.config['SQLALCHEMY_DATABASE_URI'] = CONF.database_url
# db = flask.ext.sqlalchemy.SQLAlchemy(app)
# Bootstrap(app)


@app.route('/', methods=['GET'])
def index():
    # Create random string for identification
    my_uuid = str(uuid.uuid4())
    data = {'location' : 'queue/' + my_uuid}

    # Put the job inside the rabbit queue.
    return jsonify(data), 202


@app.route('/queue/<string:jobid>', methods=['GET'])
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


def main():
    # manager.create_api(Fractal, methods=['GET', 'POST', 'DELETE', 'PUT'],
    #                    postprocessors={'POST': [generate_fractal]},
    #                    exclude_columns=['image'],
    #                    url_prefix='/v1')
    # app.run(host=CONF.listen_address, port=CONF.bind_port)
    app.run(host='0.0.0.0', port=80)

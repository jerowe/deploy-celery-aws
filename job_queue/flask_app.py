from flask import Flask
from flask import jsonify, request
from flask_cors import CORS, cross_origin
import json
import time
from celery import Celery
from flask_restful import Resource, Api, reqparse
import sys
import os


app = Flask(__name__)
CORS(app, allow_headers=['Content-Type', 'Access-Control-Allow-Origin',
                         'Access-Control-Allow-Headers', 'Access-Control-Allow-Methods'])

api = Api(app)
parser = reqparse.RequestParser()


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker='amqp://admin:mypass@rabbit:5672', backend='rpc://',
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task()
def add_together(a, b):
    time.sleep(100)
    return a + b


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
    response.headers["Access-Control-Allow-Headers"] = \
        "Access-Control-Allow-Headers,  Access-Control-Allow-Origin, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    return response


# These are just some health/server is up checks

@app.route('/', methods=['GET'])
def enter():
    return jsonify({'status': 'ok'})


@app.route('/health', methods=['POST'])
@cross_origin(origin='*')
def health():
    try:
        data = json.loads(request.data.decode('utf-8'))
        return jsonify(data)
    except Exception as e:
        return jsonify({'status': 'ok'})


class AddTogether(Resource):
    """
    Resource to trigger the add_together celery task
    """

    def post(self):
        parser.add_argument('x1', type=int, required=True)
        parser.add_argument('x2', type=int, required=True)
        args = parser.parse_args()
        add_together.delay(args.x1, args.x2)
        return {'context': {'request': args, 'path': '/add_together'}, 'sent': 1}


api.add_resource(AddTogether, '/add_together')


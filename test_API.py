#!/usr/bin/env python

from flask import Flask, jsonify, make_response, request, current_app, json
from datetime import timedelta, datetime
from functools import update_wrapper
from random import random

app = Flask(__name__)

route_root = '/api/v1.0/'


def crossdomain(origin='*', methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def gen_data(now, i):
    date = now+timedelta(days=i)
    date = date.strftime("%d-%b-%y")
    x = {'date': date, 'y_var': random()}
    return x


@app.route(route_root + 'random', methods=['GET'])
@crossdomain(headers='Content-Type')
def random_normal():
    now = datetime.now()
    x = [gen_data(now, i) for i in range(100)]
    x = {'data': x}
    return jsonify(x)


@app.route(route_root + 'echo', methods=['POST'])
def echo():
    if request.data:
        qd = json.loads(request.data)
        return jsonify(qd)
    else:
        return jsonify({'error': 'no data'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    ## Test with:
    #  curl -H "Content-Type: application/json" -X POST -d '{"foo":"bar"}' localhost:5000/api/v1.0/echo
    #  curl -H "Content-Type: application/json" -X GET localhost:5000/api/v1.0/random

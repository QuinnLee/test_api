#!/usr/bin/env python

from flask import Flask, jsonify, abort, make_response, request, url_for, current_app, json
import numpy as np


app = Flask(__name__)

route_root = '/api/v1.0/'


@app.route(route_root + 'random', methods=['GET'])
def random_normal():
    x = {'x':list(np.random.normal(0,1,100))}
    return jsonify(x)


@app.route(route_root + 'echo', methods=['POST'])
def echo():
    if request.data:
        qd = json.loads(request.data)
        return jsonify(qd)
    else:
        return jsonify({'error':'no data'})


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
    ## Test with:
    #  curl -H "Content-Type: application/json" -X POST -d '{"foo":"bar"}' localhost:5000/api/v1.0/echo
    #  curl -H "Content-Type: application/jso" -X GET localhost:5000/api/v1.0/random
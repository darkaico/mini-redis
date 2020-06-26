import os

from flask import (
    Flask,
    jsonify,
    request
)

from mini_redis import (
    CommandError,
    MiniRedis
)

app = Flask(__name__)


def create_error_response(msg):
    return jsonify({
        'error': msg
    })


def create_success_response(msg=''):
    return jsonify({
        'message': msg
    })


@app.route('/')
def index():
    return 'Hello, Android!'


@app.route(r'/api/store/<key>', methods=['GET'])
def get_key(key):
    try:
        response = MiniRedis.instance().get(key)
    except CommandError as e:
        return create_error_response(e)

    return create_success_response({
        'value': response
    })


@app.route(r'/api/store/<key>', methods=['PUT'])
def set_key(key):
    try:
        data = request.json
    except ValueError:
        return create_error_response('not a valid request data')

    value = data.get('value')

    try:
        response = MiniRedis.instance().set(key, value)
    except CommandError as e:
        return create_error_response(e)

    return create_success_response(response)


@app.route(r'/api/store/<key>', methods=['DELETE'])
def delete_key(key):
    response = MiniRedis.instance().delete(key)

    return create_success_response(response)


@app.route(r'/api/store/<key>/incr', methods=['PUT'])
def put_incr(key):
    try:
        response = MiniRedis.instance().incr(key)
    except CommandError as e:
        return create_error_response(e)

    return create_success_response(response)


@app.route(r'/api/store/<key>/zadd', methods=['PUT'])
def put_zadd(key):
    try:
        data = request.json
    except ValueError:
        return create_error_response('not a valid request data')

    score = data.get('score')
    member = data.get('member')

    try:
        response = MiniRedis.instance().zadd(key, score, member)
    except CommandError as e:
        return create_error_response(e)

    return jsonify({
        "value": response
    })


@app.route(r'/api/store/<key>/zcard')
def get_zcard(key, method=['GET']):

    try:
        response = MiniRedis.instance().zcard(key)
    except CommandError as e:
        return create_error_response(e)

    return jsonify({
        'value': response
    })


@app.route(r'/api/store/<key>/zrank/<member>', methods=['GET'])
def get_zrank(key, member):

    response = MiniRedis.instance().zrank(key, member)

    return jsonify({
        'value': response
    })


@app.route(r'/api/store/<key>/zrange', methods=['GET'])
def get_zrange(key):

    start = request.args.get('start')
    stop = request.args.get('stop')

    try:
        response = MiniRedis.instance().zrange(key, start, stop)
    except CommandError as e:
        return create_error_response(e)

    return jsonify({
        'range': response
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=8080)

import json

from aiohttp import web

from mini_redis import (
    CommandError,
    MiniRedis
)

routes = web.RouteTableDef()


def create_success(response):
    """Create simple response

    :param response: dict/str content
    :return 200 with response content
    """
    return web.Response(text=json.dumps(response))


def create_server_error(error_response: Exception):
    """Create simple server error

    :param error_response: Exception instance
    :return 500 error with message
    """
    return web.Response(text=str(error_response), status=500)


def create_request_error(error_response: CommandError):
    """Create simple command error

    :param error_response: CommandError instance
    :return 400 error with message
    """
    return web.Response(text=str(error_response), status=400)


@routes.get(r'/api/dbsize')
async def get_db_size(request):
    try:
        dbsize = MiniRedis.instance().dbsize()
    except CommandError as e:
        return create_request_error(e)

    return web.Response(text=json.dumps(dbsize))


@routes.get(r'/api/store/{key}')
async def get_key(request):
    key = request.match_info['key']

    try:
        response = MiniRedis.instance().get(key)
    except CommandError as e:
        return create_request_error(e)

    return create_success(response)


@routes.put(r'/api/store/{key}')
async def set_key(request):
    key = request.match_info['key']
    try:
        data = await request.json()
    except ValueError:
        return create_request_error('not a valid request data')

    value = data.get('value')

    try:
        response = MiniRedis.instance().set(key, value)
    except CommandError as e:
        return create_request_error(e)

    return create_success(response)


@routes.delete(r'/api/store/{key}')
async def delete_key(request):
    key = request.match_info['key']
    response = MiniRedis.instance().delete(key)

    return create_success(response)


@routes.put(r'/api/store/{key}/incr')
async def put_incr(request):
    key = request.match_info['key']

    try:
        response = MiniRedis.instance().incr(key)
    except CommandError as e:
        return create_request_error(e)

    return create_success(response)


@routes.put(r'/api/store/{key}/zadd')
async def put_zadd(request):
    key = request.match_info['key']
    score = request.query.get('score')
    member = request.query.get('member')

    try:
        response = MiniRedis.instance().zadd(key, score, member)
    except CommandError as e:
        return create_request_error(e)

    return create_success(response)


@routes.get(r'/api/store/{key}/zcard')
async def get_zcard(request):
    key = request.match_info['key']

    try:
        response = MiniRedis.instance().zcard(key)
    except CommandError as e:
        return create_request_error(e)

    return create_success(response)


@routes.get(r'/api/store/{key}/zrank/{member}')
async def get_zrank(request):
    key = request.match_info['key']
    member = request.match_info['member']

    response = MiniRedis.instance().zrank(key, member)

    return create_success(response)


@routes.get(r'/api/store/{key}/zrange')
async def get_zrange(request):

    key = request.match_info['key']
    start = request.query.get('start')
    stop = request.query.get('stop')

    try:
        response = MiniRedis.instance().zrange(key, start, stop)
    except CommandError as e:
        return create_request_error(e)

    return create_success(response)

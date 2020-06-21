import json

from aiohttp import web

from mini_redis import MiniRedis

routes = web.RouteTableDef()


@routes.get(r'/api/dbsize')
async def get_db_size(request):
    dbsize = MiniRedis.instance().dbsize()

    return web.Response(text=json.dumps(dbsize))


@routes.get(r'/api/store/{key}')
async def get_key(request):
    key = request.match_info['key']
    response = MiniRedis.instance().get(key)

    return web.Response(text=json.dumps(response))


@routes.put(r'/api/store/{key}')
async def set_key(request):
    async for line in request.content:
        value = line.decode("utf-8")

    key = request.match_info['key']
    response = MiniRedis.instance().set(key, value)

    return web.Response(text=json.dumps(response))


@routes.delete(r'/api/store/{key}')
async def delete_key(request):
    key = request.match_info['key']
    response = MiniRedis.instance().delete(key)

    return web.Response(text=json.dumps(response))


@routes.put(r'/api/store/{key}/incr')
async def put_incr(request):
    key = request.match_info['key']
    response = MiniRedis.instance().incr(key)

    return web.Response(text=json.dumps(response))


@routes.put(r'/api/store/{key}/zadd/{score:\d+}/{member}')
async def put_zadd(request):
    key = request.match_info['key']
    score = int(request.match_info['score'])
    member = request.match_info['member']

    response = MiniRedis.instance().zadd(key, score, member)

    return web.Response(text=json.dumps(response))


@routes.get(r'/api/store/{key}/zcard')
async def get_zcard(request):
    key = request.match_info['key']
    response = MiniRedis.instance().zcard(key)

    return web.Response(text=json.dumps(response))


@routes.get(r'/api/store/{key}/zrank/{member}')
async def get_zrank(request):
    key = request.match_info['key']
    member = request.match_info['member']

    response = MiniRedis.instance().zrank(key, member)

    return web.Response(text=json.dumps(response))


@routes.get(r'/api/store/{key}/zrange/{start:\d}/{stop:\d}')
async def get_zrange(request):
    key = request.match_info['key']
    start = int(request.match_info['start'])
    stop = int(request.match_info['stop'])

    response = MiniRedis.instance().zrange(key, start, stop)

    return web.Response(text=json.dumps(response))

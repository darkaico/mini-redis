from aiohttp import web
from simple_server.routes import routes


class MiniRedisServer:

    def __init__(self):
        self.app = web.Application()
        self.app.add_routes(routes)

    def start(self):
        web.run_app(self.app)


if __name__ == '__main__':
    MiniRedisServer().start()

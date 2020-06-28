from flask import Flask

from api.routes import api_routes

app = Flask(__name__)
app.register_blueprint(api_routes)


@app.route('/')
def index():
    return 'Hello, Avocado! 🥑'


if __name__ == '__main__':
    app.run(host='0.0.0.0')

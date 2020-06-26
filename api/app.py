import os

from flask import Flask

from api.routes import api_routes

app = Flask(__name__)
app.register_blueprint(api_routes)


@app.route('/')
def index():
    return 'Hello, Avocado! 🥑'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=8080)

from flask import Flask
from routes.all_routes import ALL_ROUTES
from dotenv import load_dotenv
import os


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def create_app():
    app = Flask(__name__)
    for rota in ALL_ROUTES:
        app.register_blueprint(rota)
    return app


app = create_app()

app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise RuntimeError("SECRET_KEY not found. Set it in ChatEat/.env")
if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)

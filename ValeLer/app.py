from flask import Flask
from  routes.all_routes import ALL_ROUTES
import os


def create_app():
    app = Flask(__name__)
    for rota in ALL_ROUTES:
        app.register_blueprint(rota)
    return app

try:
    app = create_app
    app.secret_key = os.getenv("SECRET_KEY")
    if __name__ == '__main__':
        port = int(os.getenv("PORT", 5000))
        debug = os.getenv("FLASK_DEBUG", "0") == "1"
        app.run(host='0.0.0.0', port=port, debug=True)
except Exception as err:
    print('Erro:',err)
finally:
    print('Rodando')

from flask import Flask
import os
from routes.home_routes import home
from routes.admin_routes import admin
try:
    app = Flask(__name__)
    app.register_blueprint(home)
    app.register_blueprint(admin)

    if __name__ == '__main__':
        port = int(os.getenv("PORT", 5000))
        debug = os.getenv("FLASK_DEBUG", "0") == "1"
        app.run(host='0.0.0.0', port=port, debug=debug)
except Exception as err:
    print('Erro:',err)
finally:
    print('Rodando')

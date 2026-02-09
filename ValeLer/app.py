from flask import Flask
import os
from routes.home_routes import home
from routes.admin_routes import admin
from routes.login_routes import login
from routes.perfil_routes import perfil
from routes.feedback_routes import feedback
try:
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.register_blueprint(home)
    app.register_blueprint(admin)
    app.register_blueprint(login)
    app.register_blueprint(perfil)
    app.register_blueprint(feedback)

    if __name__ == '__main__':
        port = int(os.getenv("PORT", 5000))
        debug = os.getenv("FLASK_DEBUG", "0") == "1"
        app.run(host='0.0.0.0', port=port, debug=True)
except Exception as err:
    print('Erro:',err)
finally:
    print('Rodando')

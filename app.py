from flask import Flask
from routes.home_routes import home
from routes.admin_routes import admin
try:
    app = Flask(__name__)
    app.register_blueprint(home)
    app.register_blueprint(admin)

    if __name__ == '__main__':
        app.run(host='localhost', port=5000,debug=True)
except Exception as err:
    print('Erro:',err)
finally:
    print('Rodando')
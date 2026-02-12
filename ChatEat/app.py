from flask import Flask
from routes.home import home_route
from routes.admin_routes import admin_route
from routes.login_routes import login_route
from routes.profile import profile_route
from routes.feedback_routes import feedback_route
from routes.carrinho_routes import carrinho_route
from routes.gatway_routes import gatway_route
from routes.entregador_routes import entregador_route
from dotenv import load_dotenv
import os


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

app = Flask(__name__)

#Rotas
app.register_blueprint(home_route)
app.register_blueprint(admin_route)
app.register_blueprint(carrinho_route)
app.register_blueprint(login_route)
app.register_blueprint(profile_route)
app.register_blueprint(feedback_route)
app.register_blueprint(gatway_route)
app.register_blueprint(entregador_route)
app.secret_key = os.getenv('SECRET_KEY')
if not app.secret_key:
    raise RuntimeError("SECRET_KEY not found. Set it in ChatEat/.env")
if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)

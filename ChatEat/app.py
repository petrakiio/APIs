from flask import Flask
from routes import home,admin_routes
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

#Var
home_route = home.home_route
admin = admin_routes.admin_route

#Rotas
app.register_blueprint(home_route)
app.register_blueprint(admin)
app.secret_key = os.getenv('SECRET_KEY')
if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)
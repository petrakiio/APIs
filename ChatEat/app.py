from flask import Flask
from routes.home import home_route
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

#Rotas
app.register_blueprint(home_route)
app.secret_key = os.getenv('SECRET_KEY')
if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)
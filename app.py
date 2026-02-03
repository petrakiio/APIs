from flask import Flask
from routes.home_routes import home

app = Flask(__name__)
app.register_blueprint(home)

if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)
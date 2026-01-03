from flask import Flask,render_template
from routes.home import home_route

app = Flask(__name__)

#Rotas
app.register_blueprint(home_route)


if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)
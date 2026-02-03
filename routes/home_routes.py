from flask import Blueprint,render_template,redirect,url_for

home = Blueprint('Home',__name__)

@home.route('/')
@home.route('/index')
def index():
    return render_template('index.html')
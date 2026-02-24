from functools import wraps
from flask import session, redirect, url_for,flash


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('Login.login'))
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('Login.login'))
        
        if not session.get('is_admin', False):
            flash("Você não tem permissão para acessar esta página.", "error")
            return redirect(url_for('home.index'))
        
        return func(*args, **kwargs)
    return wrapper

def entregador_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('Login.login'))

        if not (session.get('is_motoboy', False) or session.get('is_entregador', False)):
            flash("Você não tem permissão para acessar esta página.", "error")
            return redirect(url_for('home.index'))

        return func(*args, **kwargs)
    return wrapper

from routes.home_routes import home
from routes.admin_routes import admin
from routes.login_routes import login
from routes.perfil_routes import perfil
from routes.feedback_routes import feedback

ALL_ROUTES = {
    home,
    admin,
    login,
    perfil,
    feedback
}

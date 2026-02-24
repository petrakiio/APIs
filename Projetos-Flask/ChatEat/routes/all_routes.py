from routes.home import home_route
from routes.admin_routes import admin_route
from routes.login_routes import login_route
from routes.profile import profile_route
from routes.feedback_routes import feedback_route
from routes.carrinho_routes import carrinho_route
from routes.gatway_routes import gatway_route
from routes.entregador_routes import entregador_route

ALL_ROUTES = {
    home_route,
    admin_route,
    login_route,
    profile_route,
    feedback_route,
    carrinho_route,
    gatway_route,
    entregador_route
}
from .core import get_connection
from .auth_conn import (
    criptografar_senha,
    verificar_email,
    inserir_cliente,
    buscar_cliente,
    buscar_senha,
    deletar,
    atualizar_imagem_perfil,
)
from .cart_conn import get_user_id, get_itens_carrinho, add_carinho, del_carinho
from .feedback_conn import add_com, feeds, deletar as deletar_feedback
from .admin_conn import users_get, users_del, users_admin, users_rm_admin
from .products_conn import (
    get_products,
    search_products,
    delete_product,
    insert_product,
    update_product,
)

deletar_feedback = deletar_feedback

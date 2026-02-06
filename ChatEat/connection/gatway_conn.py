import mercadopago
from dotenv import load_dotenv
import os
import qrcode

load_dotenv()

sdk = mercadopago.SDK(os.getenv('ACESS_TOKEN'))

def create_gatway(produto):
    try:
        request_dada = {
            "items": [
                {
                    "id": int(produto["id"]),
                    "title": produto["nome"],
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": float(produto["preco"]),
                }
            ],
            "back_urls":
            {
                "success": "http://localhost:5000/sucesso",
                "failure": "http://localhost:5000/falha",
                "pending": "http://localhost:5000/pendente"
            }
        }
        response = sdk.preference().create(request_dada)
        if response.get("status") not in (200, 201):
            print(f"Mercado Pago error: {response}")
            return None
        pref = response.get("response", {})
        return pref.get("init_point") or pref.get("sandbox_init_point")
    except Exception as e:
        print(f"Error creating preference: {e}")
        return None
    finally:
        print(f"Request data: {request_dada}")

produto = {
    "id": 1,
    "nome": "Produto de Teste",
    "preco": 100.00
}
link = create_gatway(produto)
print(link)
qrcode = qrcode.make(link)
qrcode.save("qrcode.png")
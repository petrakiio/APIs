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
                    "description": produto.get("descricao", ""),
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

def generate_qr_code(url):
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save('static/img/qr_code.png')
        return img
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None
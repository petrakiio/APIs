import os
from pathlib import Path

import mercadopago
from dotenv import load_dotenv
import qrcode

load_dotenv()

sdk = mercadopago.SDK(os.getenv('ACESS_TOKEN'))
WEBHOOK_URL = os.getenv('MERCADOPAGO_WEBHOOK_URL')

_payment_status_cache = {}

def create_gatway(produto):
    request_dada = None
    try:
        request_dada = {
            "items": [
                {
                    "id": int(produto.id),
                    "title": produto.nome,
                    "description": produto.descricao or "",
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": float(produto.preco),
                }
            ],
            "back_urls":
            {
                "success": "http://localhost:5000/sucesso",
                "failure": "http://localhost:5000/falha",
                "pending": "http://localhost:5000/pendente"
            },
            "auto_return": "approved",
        }
        if WEBHOOK_URL:
            request_dada["notification_url"] = WEBHOOK_URL
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
        if request_dada is not None:
            print(f"Request data: {request_dada}")

def get_payment(payment_id):
    try:
        return sdk.payment().get(payment_id)
    except Exception as e:
        print(f"Error fetching payment: {e}")
        return None

def get_payment_status(payment_id):
    cached = _payment_status_cache.get(str(payment_id))
    if cached:
        return cached
    response = get_payment(payment_id)
    if not response or response.get("status") != 200:
        return None
    status = response.get("response", {}).get("status")
    if status:
        _payment_status_cache[str(payment_id)] = status
    return status

def set_payment_status(payment_id, status):
    if payment_id and status:
        _payment_status_cache[str(payment_id)] = status

def generate_qr_code(url, filename="qrcode.png"):
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        project_root = Path(__file__).resolve().parents[1]
        output_path = project_root / "static" / "img" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        return img
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None

def delete_qr_code(filename="qrcode.png"):
    try:
        project_root = Path(__file__).resolve().parents[1]
        file_path = project_root / "static" / "img" / filename
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting QR code: {e}")
        return False

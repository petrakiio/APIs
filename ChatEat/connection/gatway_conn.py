from abacatepay import AbacatePay
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("API_KEY")
client = AbacatePay(api_key=key)
print("AbacatePay client initialized.")
qrcode = client.pixQrCode.create({
    'amount': 10.00,
})

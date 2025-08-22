from flask import Flask, request
import os

from backend.table import create_tables
from backend.webhook_funcs import store_transaction_db
from backend.jwt_utils import get_public_key, verify_jwt_payload

app = Flask(__name__)

@app.route("/")
def home():
    return ("hi")

def init_db():
    if not os.path.exists("service.db"):
        create_tables()


@app.route("/webhook", methods=["POST"])
def receive_webhook():
    try:
        jwt_token = request.headers.get('X-JWT-Signature')
        if not jwt_token:
            return "Missing X-JWT-Signature", 400

        bank_public_key = get_public_key()
        payload_verified = verify_jwt_payload(jwt_token, bank_public_key)
        if not payload_verified:
            return "Invalid JWT Token", 401

        store_status = store_transaction_db(payload_verified)

        #send to line

        return "Transaction Received", 200

        # transfer_payload = request.get_json()
        # transaction_id = transfer_payload["transfer_id"]
        # source = transfer_payload["source"]
        # amount = transfer_payload["amount"]

        # print(f"{transaction_id}, {source}, {amount}")
        # return "Notification Received", 200
    except Exception as e:
        print(f"{e}")
        return f"Missing:{e}", 500



if __name__ == "__main__":
    init_db()
    # app.run(port=9888, debug=True)
    port = int(os.environ.get("PORT", 5678))  # Railway sets PORT
    app.run(host="0.0.0.0", port=port, debug=False)
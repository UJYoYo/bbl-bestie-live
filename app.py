from flask import Flask, request
import os

from backend.table import create_tables
from backend.webhook_funcs import store_transaction_db
from backend.jwt_utils import get_public_key, verify_jwt_payload

from flask import Flask, request, abort


from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

# LINE credentials (add these)
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
if not LINE_CHANNEL_ACCESS_TOKEN:
    print("channel access token not found")

LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
if not LINE_CHANNEL_SECRET:
    print ("secret not found")

configuration = Configuration(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/")
def home():
    return ("hi")

def init_db():
    if not os.path.exists("service.db"):
        create_tables()


@app.route("/webhook/bank", methods=["POST"])
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


@app.route("/webhook/line-oa", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    if not configuration:
        print("❌ LINE configuration not available")
        return
        
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"You said: {event.message.text}")]
                )
            )
    except Exception as e:
        print(f"❌ Error sending LINE message: {e}")

if __name__ == "__main__":
    init_db()
    # app.run(port=9888, debug=True)
    port = int(os.environ.get("PORT", 5678))  # Railway sets PORT
    app.run(host="0.0.0.0", port=port, debug=False)
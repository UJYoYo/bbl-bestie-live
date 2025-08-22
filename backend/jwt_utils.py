import jwt
import os
from datetime import datetime, timedelta

"""
- get private key 
- get public key
- sign payload
- 
"""

def get_private_key():
    path_file = "../.keys/private_key.pem"

    try:
        with open(path_file, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Private Key Error: {e}")
        return None

def get_public_key():
    path_file = "../.keys/public_key.pem"

    try:
        with open(path_file, "r") as f:
            return f.read()
    except Exception as e:
        print(f"Private Key Error: {e}")
        return None

def sign_jwt_payload(payload, private_key):
    """Sign payload with private key using RS256"""
    jwt_payload = {
        'data': payload,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iss': 'bangkok_bank_simulator'
    }

    try:
        jwt_token = jwt.encode(jwt_payload, private_key, algorithm='RS256')
        return jwt_token
    except Exception as e:
        print(f"sign_jwt_error: {e}")
        return None

######IMPORTANT, NEED TO UNDERSTAND HOW IT WORKS
def verify_jwt_payload(jwt_token, public_key):
    try:
        jwt_decode = jwt.decode(
            jwt_token,
            public_key,
            algorithms=['RS256'],
            options={'verify_exp': True}
        )
        return jwt_decode['data']
    except jwt.ExpiredSignatureError:
        print(f"JWT token expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid JWT token: {e}")
        return None
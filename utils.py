import base64
import calendar
import datetime
import hashlib
import hmac
import jwt

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, SECRET_HERE, ALGO


def get_hash(password):
    hash_digest = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),  # Convert the password to bytes
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )
    return base64.b64encode(hash_digest)


def check_password(password_hash, password):
    return hmac.compare_digest(
        base64.b64decode(password_hash),
        hashlib.pbkdf2_hmac(
            'sha256', password.encode(), PWD_HASH_SALT, PWD_HASH_ITERATIONS
        )
    )


def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, SECRET_HERE, algorithm=ALGO)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, SECRET_HERE, algorithm=ALGO)

    return {"access_token": access_token, "refresh_token": refresh_token}


def check_token(token):
    try:
        data = jwt.decode(token, SECRET_HERE, algorithms=[ALGO])
        return data
    except Exception as e:
        print(e)
        return None

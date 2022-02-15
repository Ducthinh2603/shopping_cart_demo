import hmac
from models.user_model import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    print(user_id)
    rs = UserModel.find_by_id(user_id)
    return rs

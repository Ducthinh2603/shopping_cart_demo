from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from controllers.resources import *
from models.security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'nothing'

# set expiration time
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)
app.config.setdefault('JWT_AUTH_URL_RULE', '/auth/login')
api = Api(app)

# /auth
jwt = JWT(app, authenticate, identity)

api.add_resource(LoginRequest, '/auth/register')
api.add_resource(CartItem, '/cartItem')
api.add_resource(Cart, '/cart')

if __name__ == '__main__':
    app.run(debug=True, port=5000)








from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from models import user_model, cart_model, cart_item_model



sample_user = ['firstName', 'lastName', 'username', 'password', 'email']
sample_product = ['name', 'quantity']


class LoginRequest(Resource):
    def post(self):
        rq = request.get_json()
        params = []
        try:
            for i in range(len(sample_user)):
                params.append(rq[sample_user[i]])
        except KeyError:
            return {
                "message": "Some fields missing."
            }, 404
        else:
            user = user_model.UserModel.add_user(*params)
            if user:
                return {
                    "message": "you're logged in!",
                    "username": user.username
                }, 201
            return {
                'message': 'user name used'
            }, 400


class CartItem(Resource):
    @jwt_required()
    def post(self):
        rq = request.get_json()
        header = request.headers.getlist(key="Authorization")[0].split()[1]
        try:
            _id = user_model.UserModel.id_decode(header)
            item = cart_item_model.CartItemModel.add_item_to_cart(_id, rq['productId'], rq['quantity'])
            if item:
                response = {}
                cart = cart_model.CartModel.get_cart(_id)
                response['id'] = _id
                response['cartItem'] = cart.cart_item
                response['subtotal'] = cart.subtotal
                response['total'] = cart.total
                response['vat'] = cart.vat
                return response, 201
        except KeyError as e:
            return {
                "message": "Not success"
            }, 404

    @jwt_required()
    def put(self):
        rq = request.get_json()
        header = request.headers.getlist(key="Authorization")[0].split()[1]
        try:
            _id = user_model.UserModel.id_decode(header)
            item = cart_item_model.CartItemModel.update_item_in_cart(rq['cartItemId'], rq['quantity'])
            if item:
                response = {}
                cart = cart_model.CartModel.get_cart(_id)
                response['id'] = _id
                response['cartItem'] = cart.cart_item
                response['subtotal'] = cart.subtotal
                response['total'] = cart.total
                response['vat'] = cart.vat
                return response, 201
        except KeyError as e:
            return {
                       "message": "Not success"
                   }, 404

    @jwt_required()
    def delete(self):
        rq = request.get_json()
        header = request.headers.getlist(key="Authorization")[0].split()[1]
        try:
            _id = user_model.UserModel.id_decode(header)
            item = cart_item_model.CartItemModel.delete_item(rq['cartItemId'])
            if item:
                response = {}
                cart = cart_model.CartModel.get_cart(_id)
                response['id'] = _id
                response['cartItem'] = cart.cart_item
                response['subtotal'] = cart.subtotal
                response['total'] = cart.total
                response['vat'] = cart.vat
                return response, 202
        except KeyError:
            return {
                       "message": "Not success"
                   }, 404


class Cart(Resource):
    @jwt_required()
    def get(self):
        header = request.headers.getlist(key="Authorization")[0].split()[1]
        try:
            _id = user_model.UserModel.id_decode(header)
            response = {}
            cart = cart_model.CartModel.get_cart(_id)
            if cart:
                response['id'] = _id
                response['cartItem'] = cart.cart_item
                response['subtotal'] = cart.subtotal
                response['total'] = cart.total
                response['vat'] = cart.vat
                return response, 200
            else:
                return {
                    'message': 'Not found'
                }, 400
        except KeyError:
            return {
                       "message": "Not success"
                   }, 404




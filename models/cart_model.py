import sqlite3

DB_PATH = './models/my_data.db'

class CartModel:
    def __init__(self, _id, cart_item, subtotal):
        self.vat = 0.1
        self.id = _id
        self.cart_item = cart_item
        self.subtotal = subtotal
        self.total = round(subtotal * (1 + self.vat), 2)

    @classmethod
    def get_cart(cls, _id):
        query = '''
        SELECT Cart_item.id, Cart_item.productId, Product.price, sum(Cart_item.quantity), sum(Cart_item.subtotal) FROM Cart_item 
        JOIN Product ON Cart_item.productId = Product.productId
        WHERE id = (?)
        GROUP BY Cart_item.productId
        '''
        cart_item = []
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (_id,))
            rs = cursor.fetchall()
            subtotal = 0
            if rs:
                for each in rs:
                    item = {
                        "id": each[0],
                        "productId": each[1],
                        "price": each[2],
                        "quantity": each[3],
                        "subtotal": each[4]
                    }
                    cart_item.append(item)
                    subtotal += each[4]
                return cls(_id, cart_item, subtotal)
            return None

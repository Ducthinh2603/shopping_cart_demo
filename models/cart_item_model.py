import sqlite3

DB_PATH = './models/my_data.db'

class CartItemModel:
    def __init__(self, _id, productId, price, quantity, subtotal):
        self.id = _id
        self.productId = productId
        self.price = price
        self.quantity = quantity
        self.subtotal = subtotal

    @classmethod
    def add_item_to_cart(cls, _id, productId, quantity):
        price = CartItemModel.search_price(productId)
        if price:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                add_item = '''
                    INSERT INTO Cart_item (id, productId, price, quantity, subtotal)  VALUES (?, ?, ?, ?, ?)
                '''
                subtotal = round(price * quantity, 2)
                cursor.execute(add_item, (_id, productId, price, quantity, subtotal))
                return cls(_id, productId, price, quantity, subtotal)
        return None

    @classmethod
    def update_item_in_cart(cls, cartItemId, quantity):
        item_price = '''
        SELECT price FROM Cart_item WHERE cartItemId = (?)
        '''
        update_item = f'''
            UPDATE Cart_item SET quantity = (?), subtotal = (?) WHERE cartItemId = (?)
        '''
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(item_price, (cartItemId,))
            except Exception:
                return None
            else:
                price = cursor.fetchone()[0]
                subtotal = round(price * quantity, 2)
                cursor.execute(update_item, (quantity, subtotal, cartItemId))
                for_confirm = '''
                    SELECT * FROM Cart_item WHERE cartItemId = (?)
                '''
                cursor.execute(for_confirm, (cartItemId,))
                rs = cursor.fetchone()
                return cls(*rs[1:])

    @classmethod
    def delete_item(cls, cartItemId):
        for_confirm = '''
        SELECT * FROM Cart_item WHERE cartItemId = (?)
        '''
        del_command = '''
            DELETE FROM Cart_item WHERE cartItemId = (?)
        '''
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(for_confirm, (cartItemId,))
            item = cursor.fetchone()
            if item:
                cursor.execute(del_command, (cartItemId,))
                return cls(*item[1:])
            return None

    @staticmethod
    def search_price(productId):
        search_price = '''
            SELECT price FROM Product WHERE productId = (?)
        '''
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(search_price, (productId,))
            rs = cursor.fetchone()
            if rs:
                return rs[0]
            return None


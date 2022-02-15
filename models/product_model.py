import sqlite3

DB_PATH = './models/my_data.db'


class ProductModel:
    def __init__(self, _id, name, price):
        self.id = _id
        self.name = name
        self.price = price

    # def add_product(self):
    #     with sqlite3.connect('my_data.db') as conn:
    #         c = conn.cursor()
    #         insert_command = "INSERT INTO Products VALUES (?,?,?,?)"
    #         c.execute(insert_command, (self.id, self.name, self.price, self.quantity))

    @classmethod
    def product_check(cls, name):
        product_check = '''
            SELECT * FROM Product WHERE name = (?)
        '''
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(product_check, (name,))
            rs = cursor.fetchone()
            if rs:
                return cls(*rs)
            return None

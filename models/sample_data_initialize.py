import sqlite3

with sqlite3.connect('my_data.db') as conn:
    c = conn.cursor()
    product_table = '''
    CREATE TABLE IF NOT EXISTS Product (
    productId INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    price REAL
    )'''

    cart_item = '''
    CREATE TABLE IF NOT EXISTS Cart_item (
    cartItemId INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER,
    productId INTEGER,
    price REAL,
    quantity INTEGER,
    subtotal REAL,
    FOREIGN KEY (productId) REFERENCES Product (productId),
    FOREIGN KEY (id) REFERENCES Users (id)
    )
    '''
    user = '''
    CREATE TABLE IF NOT EXISTS Users (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   firstName TEXT,
                                   lastName TEXT,
                                   username TEXT UNIQUE,
                                   password TEXT,
                                   email TEXT
                                   )'''

    cart = '''
        CREATE TABLE IF NOT EXISTS Cart (
        id INTEGER,
        subtotal REAL,
        total REAL,
        FOREIGN KEY (id) REFERENCES User (id)
        ON DELETE CASCADE
        )
        '''
    c.execute(product_table)
    c.execute(cart_item)
    c.execute(user)
    c.execute(cart)
    # Insert some sample products
    add_product = '''
    INSERT INTO Product (name, price) VALUES (?,?)
    '''
    sample = [
        ('Car', '120000'),
        ('Drum', '106'),
        ('Baseball', '12.4'),
        ('Gloves', '12.4'),
        ('Piano', '153999')
    ]
    for each in sample:
        c.execute(add_product, each)

    # c.execute('''
    # UPDATE Product SET quantity = ? WHERE name = ?''',
    #           (12, 'Book'))
    c.execute('''
    SELECT * FROM Product
    ''')
    data = c.fetchall()
    print(data)


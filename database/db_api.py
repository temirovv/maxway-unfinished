import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data


    def create_category_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL
        )'''
        self.execute(sql, commit=True)
    
    def create_products_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            weight INTEGER NOT NULL,
            ingredients VARCHAR(500),
            price REAL NOT NULL,
            image VARCHAR(500) NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES category(id)
        )'''
        self.execute(sql, commit=True)

    def create_cart_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                total_price REAL,
                quantity INTEGER,
                FOREIGN KEY (product_id) REFERENCES product(id)
        )'''
        self.execute(sql, commit=True)

    def create_user_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS user (
                tg_id INTEGER PRIMARY KEY,
                username VARCHAR(100),
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                phone_number VARCHAR(20)
            )
        '''
        self.execute(sql, commit=True)

    def create_order_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255),
                pickup_type VARCHAR(255),
                location VARCHAR(255),
                payment_type VARCHAR(255),
                detail TEXT,
                transaction_id VARCHAR(255),
                tg_id INTEGER,
                pickup_location VARCHAR(255),
                total_amount REAL, 
                status VARCHAR(30) DEFAULT "PENDING",
                created_at DATETIME
        )'''
        self.execute(sql, commit=True)

    # CATEGORY CRUD OPERATIONS
    def add_category(self, name: str) -> None:
        sql = """INSERT INTO category (name) VALUES (?)"""
        self.execute(sql, parameters=(name,), commit=True)
    
    def update_category(self,id: int, new_name: str) -> None:
        sql = '''UPDATE category SET name = ? WHERE id = ?'''
        self.execute(sql, parameters=(new_name, id), commit=True)
    
    def delete_category(self, id):
        sql = '''DELETE FROM category WHERE id = ?'''
        self.execute(sql, parameters=(id, ), commit=True)

    def select_categories(self) -> list:
        sql = '''SELECT * FROM category'''
        return self.execute(sql, fetchall=True)

    def select_category_by_id(self,id: int) -> tuple:
        sql = """SELECT name FROM category WHERE id = ?"""
        return self.execute(sql, parameters=(id, ), fetchone=True)

    def check_category(self, name: str):
        sql = """SELECT EXISTS
            (SELECT 1 FROM category WHERE name = ?);
        """
        return self.execute(sql, parameters=(name,), fetchone=True)[0]

    # PRODUCT CRUD OPERATIONS
    def add_product(self, 
                    name: str, 
                    weight: int, 
                    ingredients: str, 
                    price: float, 
                    image: str, 
                    category_id: int) -> None:
        sql = '''
        INSERT INTO product 
            (name, weight, ingredients, price, image, category_id)
        VALUES 
            (?, ?, ?, ?, ?, ?)
        '''
        self.execute(sql, parameters=(name, weight, ingredients, price, image, category_id), commit=True)

    def delete_product(self, id: int) -> None:
        sql = '''DELETE FROM product WHERE id = ?'''
        self.execute(sql, parameters=(id, ), commit=True)

    def select_products_by_category(self, category_name: str) -> list:
        sql = '''
        SELECT id, name FROM
            product
        WHERE category_id = (
            SELECT id FROM category WHERE name = ?
        )
        '''
        return self.execute(sql, parameters=(category_name,), fetchall=True)


    def select_product_by_name(self, name: str) -> tuple:
        sql = '''
        SELECT * FROM product
        WHERE name = ?
        '''
        return self.execute(sql, parameters=(name,), fetchone=True)


    def check_product(self, name: str):
        sql = """SELECT EXISTS
            (SELECT 1 FROM product WHERE name = ?);
        """
        return self.execute(sql, parameters=(name,), fetchone=True)[0]


    # CART operations
    def add_to_cart(self, user_id, product_id, quantity, total_price):
        sql = '''
            INSERT INTO cart 
                (user_id, product_id, quantity, total_price)
            VALUES
                (?,?,?,?)'''
        self.execute(sql, 
                     parameters=(user_id, product_id, quantity, total_price), 
                     commit=True)


    def select_user_cart(self, user_id):
        sql = '''
            SELECT 
            cart.id, cart.quantity, cart.total_price, product.name
            FROM cart INNER JOIN product
            ON cart.product_id = product.id
            WHERE cart.user_id = ?
        '''
        return self.execute(sql, parameters=(user_id, ), fetchall=True)

    def delete_cart_item(self, cart_id: int):
        sql = '''DELETE FROM cart WHERE id = ?'''
        self.execute(sql, parameters=(cart_id,), commit=True)

    def clear_user_cart(self, user_id: int):
        sql = '''DELETE FROM cart WHERE user_id = ?'''
        self.execute(sql, parameters=(user_id,), commit=True)

    # USER operations
    def add_user(self, tg_id, username, first_name, last_name):
        sql = '''INSERT INTO user (tg_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        '''
        self.execute(sql, parameters=(tg_id, username, first_name, last_name), 
                     commit=True)

    def check_user(self, tg_id: int) -> bool:
        sql = '''SELECT EXISTS
            (SELECT 1 FROM user WHERE tg_id = ?);
        '''
        return self.execute(sql, fetchone=True, parameters=(tg_id,))[0]

    def select_user_tg_ids(self):
        sql = '''SELECT tg_id FROM user'''
        return self.execute(sql, fetchall=True)


    # ORDER operations
    def add_order(self, tg_id, name, pickup_type, location, payment_type, detail,
                  pickup_location, total_amount):
        sql = '''
            INSERT INTO orders 
                (tg_id, name, pickup_type, location, 
                payment_type, detail,pickup_location, total_amount)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?)'''
        self.execute(
            sql,
            parameters=(tg_id, name, pickup_type, location, 
                        payment_type, detail, pickup_location, total_amount),
            commit=True
        )


    def update_order(self, status, order_id, tg_id, transaction_id = None):
        sql = '''UPDATE orders SET status=?, transaction_id=? 
        WHERE tg_id = ? AND id = ?'''
        self.execute(sql, parameters=(status, transaction_id, tg_id, order_id),
                     commit=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")

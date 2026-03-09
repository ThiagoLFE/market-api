from app.database import get_connection
from app.schemas import ProductRequest, ProductResponse, UserRequest, UserResponse, UserLogin
from app.utils import map_product, map_user
from app.security import hash_password, verify_password, create_access_token

class ProductService: 

    def register_product(self, request_product: ProductRequest):
        db = get_connection()
        cur = db.cursor()
        
        cur.execute("""
        INSERT INTO product (name, price, stock, image)
            VALUES (?, ?, ?, ?)
        """, (request_product.name, request_product.price, request_product.stock, request_product.image))
        
        db.commit()
        
        product_id = cur.lastrowid

        db.close()

        row = (product_id, request_product.name, request_product.price, request_product.stock, request_product.image)
        return ProductResponse(**map_product(row))


    def get_product_service(self, id: int):
        
        db = get_connection()
        cur = db.cursor()

        res = cur.execute("""
            SELECT * FROM product WHERE id = ?
        """, (id,))

        product = res.fetchone()

        db.close()

        if product is None:
            return None

        return ProductResponse(**map_product(product))


    def list_products(self):
        
        db = get_connection()
        cur = db.cursor()

        rows = cur.execute("SELECT * FROM product").fetchall()

        products = [ ProductResponse(**map_product(row)) for row in rows ]

        db.close()

        return products


    def edit_product(self, id: int, request_product: ProductRequest):
        
        db = get_connection()
        cur = db.cursor()

        cur.execute("""
        UPDATE product
            SET name = ?, price = ?, stock = ?
        WHERE id = ?
    """, (request_product.name, request_product.price, request_product.stock, id)) 

        db.commit()
        
        if cur.rowcount == 0:
            db.close()
            return None

        db.close()

        return ProductResponse(
            id=id,
            name=request_product.name,
            price=request_product.price,
            stock=request_product.stock
        )


    def exclude_product(self, id: int):
        db = get_connection()
        cur = db.cursor()

        cur.execute("""
            DELETE FROM product
                WHERE id = ?
        """, (id, ))
        
        db.commit()

        if cur.rowcount == 0:
            db.close()
            return None
        
        db.close()

        return "Item excluded"
    

class UserService:

    def create_user(self, user_request: UserRequest):
        db = get_connection()
        cur = db.cursor()

        # Convert the password to hash_password argon2
        encript_password = hash_password(user_request.password)

        cur.execute("""
            INSERT INTO users (name, email, hash_password, is_admin)
                VALUES (?, ?, ?, ?)
        """, (user_request.name, user_request.email, encript_password, user_request.is_admin))
        
        db.commit()
        new_user_id = cur.lastrowid
        
        db.close()

        row = (new_user_id, user_request.name, user_request.email)
        return UserResponse(**map_user(row))
    
    
    def get_token(self, auth: UserLogin) -> str | None:
        db = get_connection()
        cur = db.cursor()

        user = cur.execute("SELECT * FROM users WHERE email = ?", (auth.email, )).fetchone()

        if user is None:
            return None
        
        if verify_password(auth.password, user[3]):
            token = create_access_token({
                "sub": user[2],
                "name": user[1],
                "is_admin": user[4]
            })
            return token
        
        return None
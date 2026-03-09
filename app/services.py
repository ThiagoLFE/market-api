from app.database import get_connection
from app.schemas import ProductRequest, ProductResponse
from app.utils import map_product

def register_product(request_product: ProductRequest):
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


def get_product_service(id: int):
    
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


def get_list_products():
    
    db = get_connection()
    cur = db.cursor()

    rows = cur.execute("SELECT * FROM product").fetchall()

    products = [ ProductResponse(**map_product(row)) for row in rows ]

    db.close()

    return products


def edit_product(id: int, request_product: ProductRequest):
    
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


def exclude_product(id: int):
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
from app.schemas.Product import ProductResponse

def map_product(row):
    return ProductResponse(
        id=row[0],
        name=row[1],
        price=row[2],
        stock=row[3]
    )
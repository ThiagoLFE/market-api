def map_product(row):
    return {
        "id": row[0],
        "name": row[1],
        "price": row[2],
        "stock": row[3],
        "image": row[4]
    }

def map_user(row):
    return {
        "id": row[0],
        "name": row[1],
        "email": row[2]
    }    

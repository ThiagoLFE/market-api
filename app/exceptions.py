from fastapi import HTTPException

class EmailAlreadyExistsError(Exception):
    pass
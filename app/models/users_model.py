#esquema de modelo
from pydantic import BaseModel, EmailStr #modelo base
from typing import Union #indica que el atributopuede ser de más de un tipo
from datetime import datetime #libreria de tiempo

#modelo para la tabla Users
class User(BaseModel):
    id:Union[int,None] = None 
    email: EmailStr
    password: str
    full_name: str

class UserTerms(BaseModel):
    user_id: int
    terms_id: int
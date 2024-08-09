#esquema de modelo
from pydantic import BaseModel, EmailStr #modelo base
from typing import Union #indica que el atributopuede ser de más de un tipo
from datetime import datetime #libreria de tiempo

#modelo de usuario para registrarse
class User(BaseModel):
    id:Union[int,None] = None 
    email: EmailStr
    password: str
    full_name: str

#modelo de usuario para iniciar sesion
class Userlogin(BaseModel):
    email: str
    password: str

#modelo de usuario para aceptar terminos
class UserTerms(BaseModel):
    user_id: int
    terms_id: int
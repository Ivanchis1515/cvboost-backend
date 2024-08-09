import jwt #importa json web token
from datetime import datetime, timedelta #manejo de fechas
from typing import Dict #tipo de variables

#configuracion de la clave secreta y el algoritmo
SECRET_KEY = "KeY_$$$_Jx"  #clave segura
ALGORITHM = "HS256"

def create_jwt_token(user_id: int, full_name: str) -> str:
    # Configura la fecha de expiración del token
    expiration = datetime.utcnow() + timedelta(minutes=30)#expira el token en 30min

    #crea el payload del token
    payload = {
        "sub": user_id, #id_usuario
        "name": full_name, #fullname
        "exp": expiration #expiration
    }

    #genera el token JWT
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
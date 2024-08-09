#importaciones necesarias
from fastapi import APIRouter, HTTPException, status #enrutador, excepcioneshhtp y status
from fastapi.responses import JSONResponse #respuestasjson
from app.database_config import get_database_connection #configuracion de bd
#importaciones complemento
from app.utils.json_web_token import create_jwt_token
import bcrypt #encirptacion
from app.models.users_model import User, Userlogin, UserTerms #modelo para datos de usuario
from datetime import datetime, timezone #modelo de fechas

router = APIRouter()

#registrarse
@router.post("/register")
def registrar_usuario(user: User):
    #hash de la contraseña
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    #establecer created_at al momento actual
    user_created_at = datetime.now(timezone.utc)
    tipo_rol = "Usuario"
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        query = "INSERT INTO users (email, password_hash, full_name, tipo, created_at) VALUES (%s, %s, %s, %s, %s)"
        values = (user.email, hashed_password, user.full_name, tipo_rol, user_created_at)
        cursor.execute(query, values)
        connection.commit()

        #obtener el ID del usuario insertado
        user_id = cursor.lastrowid

        #actualizar el modelo de usuario con el ID generado
        user.id = user_id

        # Generar JWT
        token = create_jwt_token(user_id, user.full_name)

        #retornar la respuesta personalizada con status 200
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "msg": "Usuario agregado",
                "token": token
            }
        )
    except Exception as err:
        print(f"Error: {err}")#depuracion
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()

@router.post("/login")
def iniciar_sesion(login_data: Userlogin):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        #buscar el usuario por correo electrónico
        query = "SELECT id, email, password_hash, full_name, tipo FROM users WHERE email = %s"
        cursor.execute(query, (login_data.email,))
        user_record = cursor.fetchone() #extrae solo un resultado

        #si no se encuentra coincidencias
        if user_record is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")

        #extraer los datos del usuario
        user_id, email, hashed_password, full_name, tipo = user_record

        #verificar la contraseña
        if not bcrypt.checkpw(login_data.password.encode('utf-8'), hashed_password.encode('utf-8')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")

        #generar el JWT
        token = create_jwt_token(user_id, full_name)

        #retornar la respuesta con el token
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "msg": "Inicio de sesión exitoso",
                "token": token
            }
        )
    except Exception as err:
        print(f"Error: {err}") #depuración
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()

#aceptar terminos y condiciones
@router.post("/accept_terms")
def aceptar_terminos(user_terms:UserTerms):
    try:
        connection = get_database_connection() #conecta a la bd
        cursor = connection.cursor()

        #verificar si el usuario existe
        user_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(user_query, (user_terms.user_id,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        #verificar si los terminos existen
        terms_query = "SELECT * FROM TermsAndConditions WHERE id = %s"
        cursor.execute(terms_query, (user_terms.terms_id,))
        terms = cursor.fetchone()

        if not terms:
            raise HTTPException(status_code=404, detail="Terms not found")

        #insertar aceptacion de terminos
        accept_query = """
            INSERT INTO UserTerms (user_id, terms_id, accepted_at) 
            VALUES (%s, %s, NOW())
        """
        values = (user_terms.user_id, user_terms.terms_id)
        cursor.execute(accept_query, values)
        connection.commit()

        #retorna una respuesta al front
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Terms accepted successfully"}
        )
    except Exception as err:
        print(f"Error: {err}")  #depuracion
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()

#verificacion si ya acepto terminos
@router.get("/has_accepted_terms/{user_id}")
def usuario_aceptarTerminos(user_id: int):
    try:
        connection = get_database_connection() #conecta a la base de datos
        cursor = connection.cursor(dictionary=True) #convierte las respuestas en diccionarios
        
        #consulta para obtener los terminos activos
        query_terms = "SELECT id FROM TermsAndConditions WHERE terms_state = 1"
        cursor.execute(query_terms)
        active_terms = cursor.fetchone()

        #si no hay terminos
        if not active_terms:
            raise HTTPException(status_code=404, detail="No active terms found")

        terms_id = active_terms['id'] #toma la id del termino si se encontro

        #consulta para verificar si el usuario ya acepto los terminos actuales
        query_acceptance = """SELECT COUNT(*) AS count FROM UserTerms WHERE user_id = %s AND terms_id = %s"""
        cursor.execute(query_acceptance, (user_id, terms_id))
        acceptance = cursor.fetchone()

        #si acepto y hay registro
        if acceptance and acceptance['count'] > 0:
            #retorna json con contenido aceptado
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"has_accepted": True}
            )
        else:
            #de lo contrario muestro no aceptado
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"has_accepted": False}
            )
    except Exception as err:
        print(f"Error: {err}")  # depuracion
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()

#consulta un usuario en particular
@router.get("/user/{user_id}")
def get_user_by_id(user_id: int):
    try:
        connection = get_database_connection() #conecta a la bd
        cursor = connection.cursor(dictionary=True) #obtener el resultado como un diccionario

        #consulta SQL para obtener el usuario por ID
        query = "SELECT id, full_name, email, tipo FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone() #selecciona el primer registro

        #si no se encuentra
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        #retorna los datos del usuario
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=user
        )

    except Exception as err:
        print(f"Error: {err}")  # Depuración
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()
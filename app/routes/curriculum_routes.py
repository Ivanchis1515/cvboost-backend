#importaciones necesarias
from fastapi import APIRouter, HTTPException, status, File, Form, UploadFile #enrutador, excepcioneshhtp y status
from fastapi.responses import JSONResponse #respuestasjson
from app.database_config import get_database_connection #configuracion de bd
##importaciones complemento
from app.models.curriculums_model import CVUserCreate, UserInformationCreate

# Inicializa el enrutador de FastAPI
router = APIRouter()

#endpoint para crear la opcion del usuario
@router.post("/cvuser/")
def create_cvuser(cv_user: CVUserCreate):
    connection = get_database_connection()  #obtener conexion a la base de datos
    cursor = connection.cursor()

    try:
        #verificar si el usuario existe
        cursor.execute("SELECT id FROM Users WHERE id = %s", (cv_user.user_id,))
        user = cursor.fetchone() #selecciona un unico registro
        #si el usuario no existe
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        #insertar los datos en la tabla CVUser
        insert_query = """INSERT INTO CVUser (user_id, cv_id, template_name, color, created_at, updated_at) VALUES (%s, %s, %s, %s, Now(), Now())"""
        cursor.execute(insert_query, (cv_user.user_id, cv_user.cv_id, cv_user.template_name, cv_user.color))
        connection.commit()

        #obtener el ID del currículum recien creado
        created_cv_id = cursor.lastrowid

        #retornar la respuesta personalizada con status 200
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "id": created_cv_id,
                "msg": "Documento agregado",
            }
        )

    except Exception as err:
        print(f"Error: {err}")#depuracion
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()

#devuelve una plantilla
@router.get("/cvs/{template_name}")
def obten_plantilla(template_name: str):
    try:
        connection = get_database_connection()  #conecta a la base de datos
        cursor = connection.cursor(dictionary=True)  #obtener el resultado como un diccionario

        #consulta SQL para obtener el CV por nombre de plantilla
        query = "SELECT id FROM cvs WHERE template_name = %s"
        cursor.execute(query, (template_name,))
        cv = cursor.fetchone()  #selecciona el primer registro que coincida

        #si no se encuentra el CV lanzar una excepcion
        if not cv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

        #retornar los datos del CV encontrado
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=cv
        )

    except Exception as err:
        print(f"Error: {err}") #depuración
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()

@router.post("/userinformation")
async def create_user_information(user_info: UserInformationCreate):
    connection = get_database_connection()
    cursor = connection.cursor()

    try:
        insert_query = """INSERT INTO UserInformation 
                          (cvid_user_template, id_user, name, surname, city, municipality, address, colony, postal_code, phone, email, photo) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (
            user_info.cvid_user_template,
            user_info.id_user,
            user_info.name,
            user_info.surname,
            user_info.city,
            user_info.municipality,
            user_info.address,
            user_info.colony,
            user_info.postalCode,
            user_info.phone,
            user_info.email,
            user_info.photo  # Guardamos el nombre del archivo de la foto
        ))
        connection.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Información insertada"}
        )

    except Exception as err:
        print(f"Error: {err}")
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

    finally:
        cursor.close()
        connection.close()

#importaciones necesarias
from fastapi import APIRouter, HTTPException, status #enrutador, excepcioneshhtp y status
from fastapi.responses import JSONResponse #respuestasjson
from app.database_config import get_database_connection #configuracion de bd
#importaciones complemento


router = APIRouter()

@router.get("/current_terms")
def get_currentTerms():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        
        #consulta para obtener los terminos activos
        query = "SELECT * FROM TermsAndConditions WHERE terms_state = 1"
        cursor.execute(query)
        terms = cursor.fetchone() #solo debe haber un termino activo

        if terms:
            #convertir los campos de fecha a cadenas de texto
            if terms.get('effective_date'):
                terms['effective_date'] = terms['effective_date'].strftime('%Y-%m-%d')
            if terms.get('created_at'):
                terms['created_at'] = terms['created_at'].strftime('%Y-%m-%d %H:%M:%S')

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=terms
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "No active terms found"}
            )
    except Exception as err:
        print(f"Error: {err}")#depuracion
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()
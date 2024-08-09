from fastapi import FastAPI, File, UploadFile, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import os

router = APIRouter()

UPLOAD_DIRECTORY = "./uploaded_files"  # Cambia esto a una ruta adecuada para tu proyecto
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):  # "file" debe coincidir con la clave en el FormData
    if not file:
        raise HTTPException(status_code=400, detail="File not uploaded")

    try:
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"filename": file.filename}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
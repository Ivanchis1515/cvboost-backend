from fastapi import FastAPI #importa fastapi
from app.middleware.CORS import add_middleware #middleware
from app.routes.user_routes import router as user_router #ruta usuarios
from app.routes.terms_routes import router as terms_router #ruta terminos y condiciones
from app.routes.curriculum_routes import router as cvs_router #ruta de curriculums.
from app.routes.utls_routes import router as utils_router #utileria

app = FastAPI()

#middleware cors para permitir conexiones de otros entornos
add_middleware(app)

#incluir rutas
app.include_router(user_router, prefix="/users")
app.include_router(terms_router, prefix="/terms")
app.include_router(cvs_router, prefix="/cv")
app.include_router(utils_router, prefix="/utils") #esta es mi endpoint de la foto
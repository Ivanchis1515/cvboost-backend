from fastapi import FastAPI #importa fastapi
from app.middleware.CORS import add_middleware #middleware
from app.routes.user_routes import router as user_router #ruta usuarios
from app.routes.terms_routes import router as terms_router #ruta terminos y condiciones

app = FastAPI()

#middleware cors para permitir conexiones de otros entornos
add_middleware(app)

#incluir rutas
app.include_router(user_router, prefix="/users")
app.include_router(terms_router, prefix="/terms")

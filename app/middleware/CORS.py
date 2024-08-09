from fastapi.middleware.cors import CORSMiddleware #importa cors de fastapi
from fastapi import FastAPI #importa fastapi

def add_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Cambia "*" por los orígenes que desees permitir
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
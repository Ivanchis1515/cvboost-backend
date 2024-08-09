def get_uvicorn_config():
    return {
        "host": "127.0.0.1",  #direccion IP
        "port": 8000,         #puerto
        "reload": True,       #habilitar el modo de recarga automatica
    }
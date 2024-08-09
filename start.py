#archivo de arranque
#uvicorn
import uvicorn #uvicorn
from server_config import get_uvicorn_config #configuracion del servidor

if __name__ == "__main__":
    config = get_uvicorn_config()
    #importa la instancia app del modulo main con la configuracion
    uvicorn.run("app.main:app", **config)

# CvBoost Backend

## Descripción

CvBoost Backend es un proyecto de backend construido con FastAPI, diseñado para gestionar plantillas de currículum en línea. Este backend está estructurado para ofrecer una solución escalable y modular, permitiendo la integración de diferentes rutas, modelos, middleware y servicios. Está configurado para facilitar el desarrollo con recarga automática para una experiencia de desarrollo más fluida.

## Tecnologías Empleadas

- **FastAPI**: Un framework moderno y rápido para construir APIs con Python 3.7+ basado en tipos de datos estándar de Python.
- **Uvicorn**: Un servidor ASGI para correr aplicaciones web Python.
- **Pydantic**: Para validación de datos y configuración en la aplicación.
- **mysql-connector-python**: Para conectividad con bases de datos MySQL.
- **PyJWT**: Para la gestión de tokens JWT.
- **Python 3.x**: El lenguaje de programación utilizado.

## Estructura del Proyecto
El proyecto está organizado de la siguiente manera:
```
CVBackend/
│
├── app/
│ ├── init.py
│ ├── main.py
│ ├── config.py
│ ├── routes/
│ │ ├── init.py
│ │ ├── user_routes.py
│ ├── models/
│ │ ├── init.py
│ │ ├── user_model.py
│ │ └── ... # Otros archivos de modelos
│ ├── middleware/
│ │ ├── init.py
│ │ ├── auth_middleware.py
│ │ └── ... # Otros archivos de middleware
├── server_config.py
├── start.py
├── requirements.txt
└── README.md
```

## Prerrequisitos

- Python 3.7 o superior.
- Pip para la gestión de paquetes.
- Un entorno virtual (recomendado para evitar conflictos de dependencias).

## Instalación
1. **Crea y activa un entorno virtual:**
```
python -m venv <Nombreentorno-env>
Activación del entorno virtual en Windows, ejecuta: fastapi-env\Scripts\activate
Activación del entorno virtual en Unix o MacOS, ejecuta: source fastapi-env/bin/activate
```
2. **Clona el repositorio:**
   ```bash
   git clone CVBackend
   cd <NOMBRE_DEL_REPOSITORIO>
   ```
3. **Instala las dependencias**
```
pip install -r requirements.txt
```
4. **Ejecuta el proyecto**
```
cd CVBackend
python start.py
```

## Configuración del Servidor
El archivo start.py se encarga de iniciar el servidor Uvicorn con la configuración especificada en server_config.py. Puedes ajustar la configuración del servidor, como el host, el puerto y el modo de recarga, directamente en server_config.py.

## Base de Datos
El proyecto está configurado para conectarse a una base de datos MySQL. Asegúrate de que MySQL esté instalado y funcionando. La configuración de la base de datos debe especificarse en config.py en la carpeta app.

## Tutorial para el Usuario
1. **Acceso a la API:** Una vez que el backend esté corriendo, puedes acceder a la documentación interactiva de la API en http://127.0.0.1:8000/docs o la alternativa en http://127.0.0.1:8000/redoc.


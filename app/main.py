from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import auth, vehiculos, marcas, concesionarias
from .database import engine
from . import models
from sqlalchemy.exc import OperationalError

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Concesionarias",
    description="API para gestionar concesionarias de vehículos",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mantener esto para permitir cualquier origen
    allow_credentials=False,  # Cambiar de True a False
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(auth.router)
app.include_router(vehiculos.router)
app.include_router(marcas.router)
app.include_router(concesionarias.router)

# Manejador global para errores de base de datos
@app.exception_handler(OperationalError)
async def db_exception_handler(request: Request, exc: OperationalError):
    return JSONResponse(
        status_code=503,
        content={"detail": "Servicio temporalmente no disponible. Intenta más tarde."},
    )

# Manejador global para errores generales
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor."},
    )

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Concesionarias",
        "documentación": "/docs"
    }
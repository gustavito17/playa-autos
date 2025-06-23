from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, vehiculos, marcas, concesionarias
from .database import engine
from . import models

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

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Concesionarias",
        "documentación": "/docs"
    }
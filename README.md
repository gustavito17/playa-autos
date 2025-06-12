# API de Concesionarias 🚗

Sistema backend completo para la gestión de concesionarias de vehículos, desarrollado con FastAPI, PostgreSQL y subida de imágenes a Cloudinary. Ideal para proyectos de compra y venta de autos.

Incluye autenticación JWT, control de acceso, administración de vehículos, concesionarias, marcas y carga de imágenes.

Listo para producción o para integrarse con un frontend hecho en React.

## Características

- Autenticación JWT para usuarios
- Gestión de concesionarias
- Catálogo de vehículos
- Gestión de marcas
- Subida de imágenes a Cloudinary
- Base de datos PostgreSQL

## Requisitos

- Python 3.8+
- PostgreSQL
- Cuenta en Cloudinary

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd playa_autos
```

2. Crear un entorno virtual e instalar dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Crear archivo `.env` en la raíz del proyecto:
```env
DATABASE_URL=postgresql://<USUARIO>:<CONTRASEÑA>@<HOST>:<PUERTO>/<NOMBRE_BD>
SECRET_KEY=<TU_CLAVE_SECRETA>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

CLOUDINARY_CLOUD_NAME=<TU_CLOUD_NAME>
CLOUDINARY_API_KEY=<TU_API_KEY>
CLOUDINARY_API_SECRET=<TU_API_SECRET>
```

4. Crear la base de datos en PostgreSQL:
```sql
CREATE DATABASE playa_autos;
```

## Uso

1. Iniciar el servidor:
```bash
uvicorn app.main:app --reload
```

2. Acceder a la documentación:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints Principales

### Autenticación
- POST `/token` - Login de usuario
- POST `/usuarios/` - Crear nuevo usuario

### Vehículos
- GET `/vehiculos/` - Listar vehículos
- POST `/vehiculos/` - Crear vehículo
- GET `/vehiculos/{id}` - Obtener vehículo
- PUT `/vehiculos/{id}` - Actualizar vehículo
- DELETE `/vehiculos/{id}` - Eliminar vehículo
- POST `/vehiculos/{id}/imagenes/` - Subir imagen de vehículo

### Marcas
- GET `/marcas/` - Listar marcas
- POST `/marcas/` - Crear marca
- GET `/marcas/{id}` - Obtener marca

### Concesionarias
- GET `/concesionarias/` - Listar concesionarias
- POST `/concesionarias/` - Crear concesionaria
- GET `/concesionarias/{id}` - Obtener concesionaria
- PUT `/concesionarias/{id}` - Actualizar concesionaria
- POST `/concesionarias/{id}/logo` - Subir logo

## Seguridad

- Las contraseñas se almacenan hasheadas
- Autenticación mediante tokens JWT
- Validación de permisos por concesionaria
- CORS configurado (ajustar en producción)

## Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request 

## 🛠️ Tecnologías utilizadas

- **Python 3.11** – Lenguaje principal del backend  
- **FastAPI** – Framework moderno y rápido para construir APIs  
- **PostgreSQL** – Base de datos relacional  
- **SQLAlchemy** – ORM para interacción con la base de datos  
- **Cloudinary** – Servicio para almacenamiento de imágenes  
- **Uvicorn** – Servidor ASGI para correr la aplicación  
- **JWT (JSON Web Tokens)** – Autenticación y autorización  
- **Passlib** – Hasheo de contraseñas  
- **Pydantic** – Validación y serialización de datos  
- **Render** – Plataforma de despliegue  
- **CORS Middleware** – Para permitir peticiones desde el frontend  
- **dotenv** – Carga de variables de entorno desde un archivo `.env`
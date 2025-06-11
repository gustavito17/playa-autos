# API de Concesionarias

API REST desarrollada con FastAPI para gestionar concesionarias de vehículos.

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
DATABASE_URL=postgresql://user:password@localhost:5432/playa_autos
SECRET_KEY=tu_clave_secreta_para_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
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
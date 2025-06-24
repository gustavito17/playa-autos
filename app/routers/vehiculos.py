from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, auth
from ..database import get_db
from ..cloudinary_utils import upload_image

router = APIRouter(
    prefix="/vehiculos",
    tags=["vehículos"]
)

@router.post("/", response_model=schemas.Vehiculo)
async def create_vehiculo(
    vehiculo: schemas.VehiculoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    # Verificar que el usuario pertenece a la concesionaria
    if current_user.concesionaria_id != vehiculo.concesionaria_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para crear vehículos en esta concesionaria"
        )
    
    db_vehiculo = models.Vehiculo(**vehiculo.dict())
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

@router.get("/", response_model=List[schemas.Vehiculo])
async def get_vehiculos(
    skip: int = 0,
    limit: int = 100,
    estado: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Vehiculo)
    if estado:
        query = query.filter(models.Vehiculo.estado == estado)
    return query.offset(skip).limit(limit).all()

@router.get("/{vehiculo_id}", response_model=schemas.Vehiculo)
async def get_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_vehiculo

@router.put("/{vehiculo_id}", response_model=schemas.Vehiculo)
async def update_vehiculo(
    vehiculo_id: int,
    vehiculo: schemas.VehiculoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    if current_user.concesionaria_id != db_vehiculo.concesionaria_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para modificar este vehículo"
        )
    
    for key, value in vehiculo.dict().items():
        setattr(db_vehiculo, key, value)
    
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

@router.delete("/{vehiculo_id}")
async def delete_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    if current_user.concesionaria_id != db_vehiculo.concesionaria_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para eliminar este vehículo"
        )
    
    db.delete(db_vehiculo)
    db.commit()
    return {"message": "Vehículo eliminado"}

@router.post("/{vehiculo_id}/imagenes/", response_model=schemas.Imagen)
async def upload_vehiculo_image(
    vehiculo_id: int,
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    try:
        # Validar el archivo
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
            
        # Verificar tamaño del archivo (max 5MB)
        file_size = 0
        file.file.seek(0, 2)  # Ir al final del archivo
        file_size = file.file.tell()  # Obtener tamaño
        file.file.seek(0)  # Volver al inicio
        
        if file_size > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(status_code=400, detail="El archivo es demasiado grande")

        # Verificar vehículo
        print(f"Buscando vehículo con ID: {vehiculo_id}")
        db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
        if db_vehiculo is None:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        
        # Verificar permisos
        print(f"Verificando permisos - Usuario concesionaria_id: {current_user.concesionaria_id}, Vehículo concesionaria_id: {db_vehiculo.concesionaria_id}")
        if current_user.concesionaria_id != db_vehiculo.concesionaria_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para añadir imágenes a este vehículo"
            )
        
        # Subir imagen
        print("Intentando subir imagen a Cloudinary")
        image_url = await upload_image(file)
        print(f"Imagen subida exitosamente: {image_url}")
        
        # Guardar en base de datos
        print("Guardando información en la base de datos")
        db_imagen = models.Imagen(url=image_url, vehiculo_id=vehiculo_id)
        db.add(db_imagen)
        db.commit()
        db.refresh(db_imagen)
        print("Imagen guardada exitosamente en la base de datos")
        
        return db_imagen
        
    except HTTPException as he:
        # Re-lanzar excepciones HTTP
        raise he
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        # Log el error completo
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")


@router.delete("/imagenes/{imagen_id}")
async def delete_vehiculo_image(
    imagen_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    try:
        # Buscar la imagen
        db_imagen = db.query(models.Imagen).filter(models.Imagen.id == imagen_id).first()
        if db_imagen is None:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        
        # Buscar el vehículo para verificar permisos
        db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.id == db_imagen.vehiculo_id).first()
        if db_vehiculo is None:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        
        # Verificar permisos
        if current_user.concesionaria_id != db_vehiculo.concesionaria_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para eliminar esta imagen"
            )
        
        # Extraer public_id de la URL de Cloudinary para eliminar la imagen
        # URL típica: https://res.cloudinary.com/cloud_name/image/upload/v1234567890/public_id.jpg
        url_parts = db_imagen.url.split('/')
        if len(url_parts) >= 2:
            public_id = url_parts[-1].split('.')[0]  # Obtener el nombre sin extensión
            
            # Eliminar de Cloudinary
            from ..cloudinary_utils import delete_image
            await delete_image(public_id)
        
        # Eliminar de la base de datos
        db.delete(db_imagen)
        db.commit()
        
        return {"message": "Imagen eliminada exitosamente"}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error al eliminar imagen: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen: {str(e)}")
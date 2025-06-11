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
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    if current_user.concesionaria_id != db_vehiculo.concesionaria_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para añadir imágenes a este vehículo"
        )
    
    image_url = await upload_image(file)
    db_imagen = models.Imagen(url=image_url, vehiculo_id=vehiculo_id)
    db.add(db_imagen)
    db.commit()
    db.refresh(db_imagen)
    return db_imagen 
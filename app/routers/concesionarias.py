from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, auth
from ..database import get_db
from ..cloudinary_utils import upload_image

router = APIRouter(
    prefix="/concesionarias",
    tags=["concesionarias"]
)

@router.post("/", response_model=schemas.Concesionaria)
async def create_concesionaria(
    concesionaria: schemas.ConcesionariaCreate,
    db: Session = Depends(get_db)
):
    db_concesionaria = models.Concesionaria(**concesionaria.dict())
    db.add(db_concesionaria)
    db.commit()
    db.refresh(db_concesionaria)
    return db_concesionaria

@router.get("/", response_model=List[schemas.Concesionaria])
async def get_concesionarias(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    concesionarias = db.query(models.Concesionaria).offset(skip).limit(limit).all()
    return concesionarias

@router.get("/{concesionaria_id}", response_model=schemas.Concesionaria)
async def get_concesionaria(concesionaria_id: int, db: Session = Depends(get_db)):
    db_concesionaria = db.query(models.Concesionaria).filter(models.Concesionaria.id == concesionaria_id).first()
    if db_concesionaria is None:
        raise HTTPException(status_code=404, detail="Concesionaria no encontrada")
    return db_concesionaria

@router.put("/{concesionaria_id}", response_model=schemas.Concesionaria)
async def update_concesionaria(
    concesionaria_id: int,
    concesionaria: schemas.ConcesionariaCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    db_concesionaria = db.query(models.Concesionaria).filter(models.Concesionaria.id == concesionaria_id).first()
    if db_concesionaria is None:
        raise HTTPException(status_code=404, detail="Concesionaria no encontrada")
    
    if current_user.concesionaria_id != concesionaria_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para modificar esta concesionaria"
        )
    
    for key, value in concesionaria.dict().items():
        setattr(db_concesionaria, key, value)
    
    db.commit()
    db.refresh(db_concesionaria)
    return db_concesionaria

@router.post("/{concesionaria_id}/logo", response_model=schemas.Concesionaria)
async def upload_logo(
    concesionaria_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    db_concesionaria = db.query(models.Concesionaria).filter(models.Concesionaria.id == concesionaria_id).first()
    if db_concesionaria is None:
        raise HTTPException(status_code=404, detail="Concesionaria no encontrada")
    
    if current_user.concesionaria_id != concesionaria_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para modificar esta concesionaria"
        )
    
    logo_url = await upload_image(file)
    db_concesionaria.logo_url = logo_url
    db.commit()
    db.refresh(db_concesionaria)
    return db_concesionaria 
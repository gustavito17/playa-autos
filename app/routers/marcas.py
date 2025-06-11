from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter(
    prefix="/marcas",
    tags=["marcas"]
)

@router.post("/", response_model=schemas.Marca)
async def create_marca(
    marca: schemas.MarcaCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    db_marca = db.query(models.Marca).filter(models.Marca.nombre == marca.nombre).first()
    if db_marca:
        raise HTTPException(status_code=400, detail="Marca ya existe")
    
    db_marca = models.Marca(**marca.dict())
    db.add(db_marca)
    db.commit()
    db.refresh(db_marca)
    return db_marca

@router.get("/", response_model=List[schemas.Marca])
async def get_marcas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    marcas = db.query(models.Marca).offset(skip).limit(limit).all()
    return marcas

@router.get("/{marca_id}", response_model=schemas.Marca)
async def get_marca(marca_id: int, db: Session = Depends(get_db)):
    db_marca = db.query(models.Marca).filter(models.Marca.id == marca_id).first()
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return db_marca 
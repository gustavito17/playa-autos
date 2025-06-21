from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import schemas, models, auth
from ..database import get_db
import traceback

router = APIRouter(tags=["autenticación"])

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/api/usuarios/me", response_model=schemas.Usuario)
async def get_current_user_info(
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    """Obtener información del usuario autenticado"""
    return current_user

@router.post("/usuarios/", response_model=schemas.Usuario)
async def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si la concesionaria existe
        concesionaria = db.query(models.Concesionaria).filter(models.Concesionaria.id == user.concesionaria_id).first()
        if not concesionaria:
            raise HTTPException(status_code=404, detail=f"Concesionaria con id {user.concesionaria_id} no encontrada")

        # Verificar si el email ya existe
        db_user = db.query(models.Usuario).filter(models.Usuario.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email ya registrado")
        
        # Crear el usuario
        hashed_password = auth.get_password_hash(user.contraseña)
        db_user = models.Usuario(
            email=user.email,
            nombre=user.nombre,
            contraseña=hashed_password,
            concesionaria_id=user.concesionaria_id
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"Error al crear usuario: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}"
        )
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Esquemas para Concesionaria
class ConcesionariaBase(BaseModel):
    nombre: str
    logo_url: Optional[str] = None
    color_principal: Optional[str] = None

class ConcesionariaCreate(ConcesionariaBase):
    pass

class Concesionaria(ConcesionariaBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para Usuario
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    contraseña: str
    concesionaria_id: int

class Usuario(UsuarioBase):
    id: int
    concesionaria_id: int

    class Config:
        from_attributes = True

# Esquemas para autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Esquemas para Marca

class MarcaBase(BaseModel):
    nombre: str

class MarcaUpdate(BaseModel):
    nombre: str

class MarcaCreate(MarcaBase):
    pass

class Marca(MarcaBase):
    id: int

    class Config:
        from_attributes = True

# Esquemas para Vehículo
class VehiculoBase(BaseModel):
    modelo: str
    anio: int
    color: str
    estado: str
    precio: int
    descripcion: str
    marca_id: int
    concesionaria_id: int

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    id: int
    imagenes: List["Imagen"] = []

    class Config:
        from_attributes = True

# Esquemas para Imagen
class ImagenBase(BaseModel):
    url: str
    vehiculo_id: int

class ImagenCreate(ImagenBase):
    pass

class Imagen(ImagenBase):
    id: int

    class Config:
        from_attributes = True

# Actualizar las referencias forward
Vehiculo.model_rebuild() 
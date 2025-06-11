from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Concesionaria(Base):
    __tablename__ = "concesionarias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    logo_url = Column(String)
    color_principal = Column(String)

    usuarios = relationship("Usuario", back_populates="concesionaria")
    vehiculos = relationship("Vehiculo", back_populates="concesionaria")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String, unique=True, index=True)
    contraseña = Column(String)
    concesionaria_id = Column(Integer, ForeignKey("concesionarias.id"))

    concesionaria = relationship("Concesionaria", back_populates="usuarios")

class Marca(Base):
    __tablename__ = "marcas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    vehiculos = relationship("Vehiculo", back_populates="marca")

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    modelo = Column(String, index=True)
    anio = Column(Integer)
    color = Column(String)
    estado = Column(String)  # usado, 0km, importado
    precio = Column(Integer)
    descripcion = Column(Text)
    marca_id = Column(Integer, ForeignKey("marcas.id"))
    concesionaria_id = Column(Integer, ForeignKey("concesionarias.id"))

    marca = relationship("Marca", back_populates="vehiculos")
    concesionaria = relationship("Concesionaria", back_populates="vehiculos")
    imagenes = relationship("Imagen", back_populates="vehiculo")

class Imagen(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"))

    vehiculo = relationship("Vehiculo", back_populates="imagenes") 
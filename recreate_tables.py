from app.database import engine
from app import models

# Eliminar todas las tablas existentes
models.Base.metadata.drop_all(bind=engine)

# Crear todas las tablas nuevamente
models.Base.metadata.create_all(bind=engine)

print("¡Tablas recreadas exitosamente!") 
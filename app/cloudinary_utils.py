import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

async def upload_image(file: UploadFile) -> str:
    """
    Sube una imagen a Cloudinary y retorna la URL
    """
    try:
        # Subir el archivo a Cloudinary
        result = cloudinary.uploader.upload(file.file)
        return result["secure_url"]
    except Exception as e:
        raise Exception(f"Error al subir imagen a Cloudinary: {str(e)}")

async def delete_image(public_id: str) -> bool:
    """
    Elimina una imagen de Cloudinary usando su public_id
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result["result"] == "ok"
    except Exception as e:
        raise Exception(f"Error al eliminar imagen de Cloudinary: {str(e)}") 
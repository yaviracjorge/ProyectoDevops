# Usar una imagen oficial de Python en su versión Alpine (extremadamente liviana)
FROM python:3.11-alpine

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar las dependencias de Python sin guardar caché de pip para reducir espacio
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al contenedor
COPY app.py .

# Eliminar carpetas innecesarias dentro del contenedor (como el entorno virtual local)
RUN rm -rf venv

# Exponer el puerto en el que corre Flask
EXPOSE 5000

# Variables de entorno para asegurar que la salida se muestre en consola sin búfer
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
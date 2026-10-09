# Imagen base oficial de Python
FROM python:3.14-slim

# Evitar que Python escriba archivos .pyc y forzar buffer de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la aplicación
COPY . .

# Exponer el puerto donde corre FastAPI
EXPOSE 8000

# Comando para iniciar la API con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
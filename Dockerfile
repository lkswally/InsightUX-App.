# Usamos una imagen ligera de Python
FROM python:3.9-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos necesarios
COPY requirements.txt .
COPY app.py .
# Si tenés el logo o más archivos, descomentá la siguiente línea:
# COPY . .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto de Streamlit
EXPOSE 8501

# Comando para iniciar la app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
FROM python:3.11-slim

WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script
COPY red_neuronal.py .

# Ejecutar el script
CMD ["python", "red_neuronal.py"]

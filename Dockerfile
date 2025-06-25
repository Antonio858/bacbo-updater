FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar todos los archivos del proyecto al contenedor
COPY . /app

# Instalar dependencias del sistema necesarias para algunas bibliotecas Python
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    default-libmysqlclient-dev \
    curl \
    git \
    && apt-get clean

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Comando para ejecutar el actualizador de datos
CMD ["python", "update_data.py"]

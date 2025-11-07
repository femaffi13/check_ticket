# Imagen base con Python
FROM python:3.11-slim

# Evita prompts interactivos de apt
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome estable
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Instalar ChromeDriver compatible
RUN CHROME_VERSION=$(google-chrome --version | grep -oP "\d+\.\d+\.\d+") \
    && DRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION%%.*}") \
    && wget -q "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código al contenedor
COPY . /app
WORKDIR /app

# Ejecutar tu script
CMD ["python", "tu_script.py"]

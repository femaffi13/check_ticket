# Imagen base con Python
FROM python:3.11-slim

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxshmfence1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libnss3 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome estable (desde el canal oficial)
RUN wget -q -O /usr/share/keyrings/google-linux-signing-keyring.gpg https://dl.google.com/linux/linux_signing_key.pub && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Instalar ChromeDriver compatible con Chrome 142 (mirror alternativo si falla Google)
RUN CHROMEDRIVER_VERSION="142.0.7444.64" && \
    set -e && \
    echo "Descargando ChromeDriver ${CHROMEDRIVER_VERSION}..." && \
    (wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O chromedriver.zip || \
     wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O chromedriver.zip) && \
    unzip -o chromedriver.zip || (echo "Fallo al descomprimir ChromeDriver, revisa la URL" && exit 1) && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver.zip chromedriver-linux64


# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . /app
WORKDIR /app

# Ejecutar tu script
CMD ["python", "check.py"]



# Use a imagem base do Python 3.13.2
FROM python:3.13.2-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt para o container
COPY requirements.txt .

# Instala as dependências do sistema necessárias (incluindo ffmpeg)
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Instala as dependências do Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante dos arquivos do projeto para o container
COPY . .

# Define o comando padrão ao iniciar o container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
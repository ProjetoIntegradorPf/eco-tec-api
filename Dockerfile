# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt requirements.txt

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do diretório atual para o diretório de trabalho
COPY . .

# Define o arquivo principal da aplicação Flask
ENV FLASK_APP=main.py

# Expõe a porta 5000, que é a porta padrão do Flask
EXPOSE 5000

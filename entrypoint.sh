#!/bin/sh

# Este script é responsável por inicializar o servidor da API Python.

echo "Verificando o conteúdo do diretório /app"
cd ./app && ls -la .

echo "Iniciando o servidor"
exec python3 main.py

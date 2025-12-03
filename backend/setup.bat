@echo off
echo Iniciando configuracao do MISOUT...
echo.

echo Instalando bibliotecas Python...
pip install Flask==2.3.3
pip install Flask-CORS==4.0.0
pip install mysql-connector-python==8.1.0
pip install bcrypt==4.0.1

echo.
echo Configurando banco de dados...
python DatabaseSetup.py

echo.
echo Configuracao concluida!
echo.
echo Execute agora: python app.py
pause
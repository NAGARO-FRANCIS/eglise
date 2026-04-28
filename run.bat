@echo off
setlocal enabledelayedexpansion

echo.
echo ====================================
echo   Application de Gestion d'Eglise
echo ====================================
echo.
echo Commandes disponibles:
echo 1. Demarrer le serveur
echo 2. Creer un superutilisateur
echo 3. Charger les donnees de demo
echo 4. Appliquer les migrations
echo 5. Creer les migrations
echo 6. Shell Django
echo 7. Quitter
echo.

set /p choice="Entrez votre choix (1-7): "

if "%choice%"=="1" (
    echo.
    echo Demarrage du serveur...
    echo Acces: http://localhost:8000
    echo.
    python manage.py runserver
) else if "%choice%"=="2" (
    echo.
    echo Creation d'un superutilisateur...
    python manage.py createsuperuser
) else if "%choice%"=="3" (
    echo.
    echo Chargement des donnees de demonstration...
    python manage.py shell < load_demo_data.py
) else if "%choice%"=="4" (
    echo.
    echo Application des migrations...
    python manage.py migrate
) else if "%choice%"=="5" (
    echo.
    echo Creation des migrations...
    python manage.py makemigrations
) else if "%choice%"=="6" (
    echo.
    echo Ouverture du shell Django...
    python manage.py shell
) else if "%choice%"=="7" (
    echo.
    echo Au revoir!
    exit /b 0
) else (
    echo.
    echo Choix invalide!
    goto :EOF
)

pause

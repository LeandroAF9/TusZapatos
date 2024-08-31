import os

# Configuración de la base de datos MySQL
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'  # Cambia esto si tu usuario es diferente
MYSQL_PASSWORD = 'nueva_contraseña'  # Cambia esto con tu contraseña
MYSQL_DB = 'tuzapatos'

# Llave secreta para las sesiones
SECRET_KEY = os.urandom(24)

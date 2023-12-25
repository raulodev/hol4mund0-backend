# Hol4 Mund0 (backend)

Creado con Django y DRF

[Visitar página](https://hol4mund0.vercel.app/)

### Instalación

```
git clone https://github.com/raulodev/hol4mund0-backend.git
```

```
cd hol4mund0-backend/
```

Crear entorno virtual

```
python3 -m venv .venv
```

Activar entorno virtual

```
source .venv/bin/activate
```

Instalar dependencias

```
pip install -r requirements.txt
```

### Crear un archivo (.env) con las siguientes variables de entorno:

`SECRET_KEY` : puedes generar una clave secreta con el siguiente comando en la terminal

```
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

`DEBUG` : Puede ser 1 (en desarrollo) o 0 (para producción)

`CONSUMER_KEY` : Clave de consumo de tu aplicación de Twitter para obtener esta [visitar portal de desarrollador](https://developer.twitter.com/en/portal/dashboard)

`CONSUMER_SECRET` : Clave de consumo secreta de tu aplicación de Twitter para obtener [visitar portal de desarrollador](https://developer.twitter.com/en/portal/dashboard)

`API_BASE_URL` : URL base de tu API por defecto es http://127.0.0.1:8000/api

Ejemplo:

```
API_BASE_URL=https://backend.miblog.com/api
```

`ALLOWED_HOSTS` : Dominio donde corre tu backend terminado con una coma (,)

Ejemplo

```
ALLOWED_HOSTS=backend.miblog.com,
```

`CORS_ALLOWED_ORIGINS` : Dominio donde corre tu frontend separado o terminado en una coma (,)

Ejemplo

```
CORS_ALLOWED_ORIGINS=https://miblog.com,
```

Variables de entorno relacionadas con la base de datos:

`SQL_ENGINE` : Motor de la base de datos (ej: django.db.backends.sqlite3)

`SQL_DATABASE` : Nombre de la base de datos

`SQL_USER` : Usuario de la base de datos

`SQL_PASSWORD` : Contraseña de la base de datos

`SQL_HOST`: Host de la base de datos

`SQL_PORT` : Puerto de la base de datos por defecto es: 5432

### Obtener archivos estáticos

```
python manage.py collectstatic
```

### Levantar servidor

Con gunicorn:

```
gunicorn backend.wsgi:application --bind 0.0.0.0:8080
```

Con el servidor de desarrollo de Django:

```
python manage.py runserver 0.0.0.0:8080
```

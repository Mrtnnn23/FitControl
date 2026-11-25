# FitControl

Proyecto de Ingeniería de Software para administrar un gimnasio. Permite registrar socios y entrenadores, gestionar membresías y pagos, organizar clases y llevar el control de reservas y asistencias.

El administrador gestiona los registros y crea las cuentas. Los socios pueden consultar su membresía y reservar clases; los entrenadores revisan sus clases y registran la asistencia.

Está desarrollado con Python, Django, HTML, CSS y JavaScript. Usa PostgreSQL en Supabase y también permite trabajar con MariaDB en local.

## Cómo ejecutarlo

Crea tu propia base de datos y configura la conexión en `.env.local`. Puedes usar `DATABASE_URL` para PostgreSQL o las variables `DB_NAME`, `DB_USER` y `DB_PASSWORD` para MariaDB. En `.env.example` hay una referencia de las variables.

Desde la carpeta donde está `manage.py`:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Al crear el administrador, ingresa un correo para poder iniciar sesión. Luego abre http://127.0.0.1:8000/.

## Pruebas

En PowerShell:

```powershell
$env:FITCONTROL_SQLITE="1"
python manage.py test gimnasio
```

Las pruebas usan una base temporal. Los datos del proyecto son ficticios; las contraseñas y los respaldos quedan fuera del repositorio.

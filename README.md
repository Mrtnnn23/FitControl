# FitControl

Aplicación de gestión de gimnasio con Django y PostgreSQL en Supabase. Incluye cuentas de administrador, socios y entrenadores; membresías, pagos administrativos, clases, reservas, asistencias y reportes.

## Publicación en Vercel

1. Importar este repositorio y seleccionar Django. La raíz debe contener `manage.py`.
2. Configurar `DATABASE_URL` y `DJANGO_SECRET_KEY` en las variables de entorno del proyecto.
3. Publicar. Vercel detecta WSGI y ejecuta `collectstatic`; los archivos se sirven desde su CDN.
4. Comprobar inicio y cierre de sesión, permisos, reservas y archivos estáticos en el enlace final.

La base de Supabase ya está migrada. El despliegue no crea cuentas ni reemplaza registros. Las migraciones futuras se ejecutan de forma controlada con `python manage.py migrate` contra el destino elegido.

## Desarrollo local

Instalar las dependencias de `requirements.txt`. MariaDB sigue siendo la opción local cuando no se configura `DATABASE_URL`. Las credenciales locales se guardan en `.env.local`, ignorado por Git. Para conectar a PostgreSQL se puede definir `DATABASE_URL` en ese archivo.

`python manage.py runserver`

## Pruebas

En PowerShell:

```powershell
$env:FITCONTROL_SQLITE="1"
python manage.py test gimnasio
```

La suite usa una base temporal. Las cuentas y los datos del proyecto son ficticios. Las contraseñas y los respaldos no se incluyen en este repositorio.

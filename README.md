# AsisteCosas que recordar en el terminal:

Para iniciar la aplicacion debo estar en la carpeta "asistente virtual"
✅cd asistentevirtual
Luego si correr: ✅python manage.py runserver asistente.local:8000

activar entorno virtual: ✅.\.venv\Scripts\activate
desactivar entorno virtual: ✅deactivate

# Access the variable using os.environ.get() to avoid KeyErrors if it's missing
my_variable = os.environ.get("MY_VAR")

if my_variable is None:
    # Handle the case where the variable is not set
    raise Exception("MY_VAR environment variable not set")

print(f"The value of MY_VAR is: {my_variable}")
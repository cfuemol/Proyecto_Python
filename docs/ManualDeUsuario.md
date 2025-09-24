# Manual de Usuario

## Introducción
La aplicación empieza con una página de login a la que se podrá acceder a un registro de usuario. En esta aplicación hay tres tipos de usuarios: administrador, empleado y cliente. Al registrarse todos los usuarios empiezan como tipo cliente. Solo el administrador puede cambiar el rol de usuario.
Usos de cada usuario:
- Administrador: En la pantalla aparece un menú en la parte izquierta donde hay un icono de inicio que te lleva a la página principal, un botón de logout para ir a la página de login y un botón para modificar usuarios. Al pulsar en ese botón te manda a la página admin_users.html. En ésta pagina aparecen los usuarios que hay en la base de datos MongoDB y a cada usuario se puede editar o borrar.
- Empleado: En la pantalla aparece un menú con los clientes registrados en la aplicación, y un botón donde puede ver las cuentas de cada cliente, puede editar y borrar cuentas de ese usuario. En el menu lateral está el botón de logout para volver a la página de login.
- Cliente: En la pantalla aparece la información del cliente, en el menú lateral tiene un botón para ir a la página de transferencias donde puede hacer transferencias entre cuentas, en el menú el icono de efectivo para retirar efectivo de una cuenta.

## Acceso y Navegación
- En consola es necesario usar el siguiente comando:
```bash
python app.py
```
- URL de acceso: `http://localhost:5000`
- Para loguearse en la página debes haberte registrado previamente, para ello pulsa en Don`t have a account y rellenas los campos de registro, si es correcto al mandarte de nuevo a la pagina de login rellena los campos y navega por la página.

## Funcionalidades CRUD
### Crear
- Al arrancar la aplicación crea la base de datos, las colecciones y un usuario administrador si no existe. 
- El usuario empleado puede crear cuentas de un usuario.
- El usuario cliente puede crear transferencias entre cuentas registradas en la base de datos.

### Leer
- El usuario administrador puede leer la información de todos los usuarios de la base de datos.
- El usuario empleado puede leer la información de las cuentas de un usuario.
- El usuario Cliente puede leer su información de usuario y sus cuentas.

### Actualizar
- El usuario administrador puede actualizar la información de un usuario cambiando el nombre, apellidos y/o rol del usuario.
- El usuario empleado puede actualizar la información de la cuenta de un usuario cambiando el dni del titular o el teléfono.
- El usuario cliente puede actualizar saldos de sus propias cuentas retirando efectivo de la que elija.

### Eliminar
- El usuario administrador puede eliminar las cuentas de usuarios.
- El usuario empleado puede eliminar cuentas de un usuario.

## Preguntas Frecuentes (FAQ)
- Compatibilidad con sistemas Operativos.
    La aplicación es compatible con todos los sistemas operativos, tanto Windows, Linux o MacOS.
- Conexión a Internet.
    Se necesita conexión a Internet para que la base de datos se conecte correctamente, en futuras versiones se implementará una base de datos de forma local.
- Actualización de datos de cliente. 
    Los datos de acceso a la base de datos se le proporcionará al cliente para que actualice sus datos de acceso y configurar la aplicación con esos datos.

## Consejos y Advertencias
- La aplicación web está optimizada para navegadores con base chromium.


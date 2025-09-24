# Proyecto_Python   PythonBank

# Notas de uso de la Aplicación

## Descripción del Proyecto

Este Proyecto trata de hacer una aplicación que gestione las actividades de un banco:
- Crear cuentas de clientes.
- Crear usuarios.
- Gestionar los datos de los usuarios que pueden ser clientes, empleados o administrador incluso poder cambiar su rol con la APP.
- Abrir cuentas bancarias a los clientes.
- Ingresar o retirar dinero en una cuenta.
- Realizar transacciones entre dos cuentas.
- El proyecto está pensado para suministrar al cliente todo lo necesario para su funcionamiento tanto la app como la base de datos MongoDB con la cuenta ya creada yconfigurada.

## Programas Necesarios

- [Python](https://www.python.org/).
- [Flask](https://flask.palletsprojects.com/)
- [MongoDB](https://https://www.mongodb.com/products/tools/compass)

## Estructura del Proyecto
```
/Proyecto_Python
├─ models/
├   └─ database.py
├─ static/
├   ├─ styles_base.css
├   └─ styles_register.css
├─ templates/
├   ├─ admin/
├   ├  ├─ admin_users.html
├   ├  ├─ dashboard_admin.html
├   ├  └─ editar_usuario.html
├   ├─ empleado/
├   ├   ├─ cuentas_cliente.html
├   ├   ├─ dashboard_empleado.html
├   ├   └─ edtar_cuenta.html
├   ├─ usuario/
├   ├   ├─ crear_transferencia.html
├   ├   ├─ dashboard_cliente.html
├   ├   ├─ efectivo.html
├   ├   └─ transferencia.html
├   ├─ 404.html
├   └─ register.html
├─ .env
├─ app.py
├─ README.md
├─ requirements.txt
└─ docs/
    ├─ ManualDeUsuario.md
    └─ DocumentacionTecnica.md
```

## Instalación del Entorno de Desarrollo
```bash
# Crear entorno virtual
python3 -m venv venv
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución Local de la Aplicación
```bash
python app.py
```

## Créditos y Contacto

Autores:
- José Ignacio Barranco Ruiz.
- Cristóbal Fuentes Molina.

Contacto:
- jbarrui587@g.educaand.es
- cfuemol584@g.educaand.es

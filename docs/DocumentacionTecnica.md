# Documentación Técnica

## Arquitectura Interna
<!-- Explicación de rutas, modelos y flujos -->

1. Login/Register
    - En este
2. Dashboard_Cliente
3. Dashboard_Empleado
4. Dashboard_Administrador
5. Logout



## Configuración y Conexión con MongoDB
<!-- Instrucciones para crear la base de datos y conectar la app -->

## Endpoints
| Ruta                          |Método             |Parámetros                     |Respuesta          |Descripción                            |
|-------------------------------|-------------------|-------------------------------|-------------------|---------------------------------------|
| /                             |GET/POST           | -                             |HTML               | Login/Register                        |
| /dashboard_cliente            |GET                | dni                           |HTML               | Landing page para clientes            |
| /transferencias/<dni>         |GET/POST           | dni,origen,destino,monto      |HTML               | Mostrar transferencias de un cliente  |
| /efectivo                     |GET/POST           | dni,origen,monto              |HTML               | Ingreso/retirada de efectivo          |
| /dashboard_admin              |GET                | dni                           |HTML               | Landing page para administradores     |
| /admin_users/<user>/edit      |GET/POST           | dni,nombre,apellidos,rol      |HTML               | Actualizar datos y/o rol de usuarios  |
| /admin_users/<user>/delete    |POST               | dni                           |HTML               | Borrar usuario de la BD               |
| /dashboard_empleado           |GET                | dni                           |HTML               | Landing page para empleados           |
| /cuentas_cliente/<cliente>    |GET                | dni                           |HTML               | Obtener cuentas del cliente           |
| /crear_cuenta/<dni>           |POST               | dni                           |HTML               | Crear una cuenta para el cliente      |
| /editar_cuenta/<id_cuenta>    |GET/POST           | dni,id_cuenta                 |HTML               | Cambiar titular de la cuenta y datos  |
| /borrar_cuenta/<id_cuenta>    |POST               | dni,id_cuenta                 |HTML               | Eliminar cuenta del usuario           |
| /logout                       |GET/POST           | -                             |HTML               | Cerrar sesión del usuario             |

## Fragmentos de Código de Ejemplo
```python
# Ejemplo de ruta en Flask
@app.route('/')
def index():
    return render_template('index.html')
```

## Notas Técnicas
<!-- Comentarios HTML y aclaraciones técnicas -->

## Referencias
<!-- Enlaces internos y externos relevantes -->

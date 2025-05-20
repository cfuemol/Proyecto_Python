-- Activar claves foráneas (necesario en SQLite)
PRAGMA foreign_keys = ON;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    dni TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    telefono TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    nombre_usuario TEXT UNIQUE NOT NULL,
    passw TEXT NOT NULL,
    rol TEXT DEFAULT '' CHECK (rol IN ('admin', 'empleado', 'cliente', ''))
);

-- Crear tabla de cuentas bancarias
CREATE TABLE IF NOT EXISTS cuentas_bancarias (
    id_cuenta INTEGER PRIMARY KEY AUTOINCREMENT,
    dni_titular TEXT NOT NULL,
    telefono TEXT UNIQUE NOT NULL,
    saldo REAL DEFAULT 0.0,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (dni_titular) REFERENCES usuarios(dni)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Crear tabla de transacciones
CREATE TABLE IF NOT EXISTS transacciones (
    id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
    cuenta_origen INTEGER NOT NULL,
    cuenta_destino INTEGER NOT NULL,
    concepto TEXT NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    monto REAL NOT NULL,
    FOREIGN KEY (cuenta_origen) REFERENCES cuentas_bancarias(id_cuenta)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (cuenta_destino) REFERENCES cuentas_bancarias(id_cuenta)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Insertar usuarios
INSERT INTO usuarios (dni, nombre, apellidos, telefono, email, nombre_usuario, passw, rol)
VALUES 
    ('12345678A', 'Juan', 'Pérez Gómez', '600112233', 'juan@example.com', 'juanp', 'clave123', 'cliente'),
    ('87654321B', 'María', 'López Ruiz', '600223344', 'maria@example.com', 'marial', 'clave456', 'cliente');

-- Insertar cuentas bancarias
INSERT INTO cuentas_bancarias (dni_titular, telefono, saldo)
VALUES 
    ('12345678A', '600112233', 1500.75),
    ('87654321B', '600223344', 2000.00);

-- Insertar una transacción entre las dos cuentas
INSERT INTO transacciones (cuenta_origen, cuenta_destino, concepto, monto)
VALUES (1, 2, 'Transferencia entre clientes', 250.00);

-- CONSULTAS DE EJEMPLO ------------------------------------------

-- Consultar usuarios y sus saldos
SELECT u.nombre, u.apellidos, cb.saldo
FROM usuarios u
JOIN cuentas_bancarias cb ON u.dni = cb.dni_titular;

-- Ver transacciones de un usuario
SELECT t.id_transaccion, t.concepto, t.monto, t.fecha
FROM transacciones t
JOIN cuentas_bancarias cb ON t.cuenta_origen = cb.id_cuenta
WHERE cb.dni_titular = '12345678A';

-- Transferencias con nombres de origen y destino
SELECT t.*, u1.nombre AS origen, u2.nombre AS destino
FROM transacciones t
JOIN cuentas_bancarias cb1 ON t.cuenta_origen = cb1.id_cuenta
JOIN cuentas_bancarias cb2 ON t.cuenta_destino = cb2.id_cuenta
JOIN usuarios u1 ON cb1.dni_titular = u1.dni
JOIN usuarios u2 ON cb2.dni_titular = u2.dni;

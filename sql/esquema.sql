CREATE DATABASE IF NOT EXISTS maquillaje_db;
USE maquillaje_db;

-- Tabla: usuarios (Sistema de Login - Semana 14)
-- Las contraseñas se guardan con hash (generate_password_hash), nunca en texto plano.
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    empresa VARCHAR(100) NOT NULL,
    contacto VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    ciudad VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    descripcion TEXT,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    estado VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL,
    id_cliente INT,
    fecha DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE
);

INSERT INTO proveedores (empresa, contacto, telefono, ciudad) VALUES
('Distribuidora Belleza S.A.', 'Carlos Ruiz', '022345678', 'Quito');

INSERT INTO clientes (nombre, email, telefono, estado) VALUES
('María López', 'maria@email.com', '0991234567', 'Activo'),
('Ana Torres', 'ana@email.com', '0997654321', 'Activo'),
('Sofia Benítez', 'sofia@email.com', '0994455667', 'Activo'),
('Camila Andrade', 'camila@email.com', '0978899001', 'Inactivo'),
('Valeria Mendoza', 'valeria@email.com', '0962233445', 'Activo');

INSERT INTO facturas (numero, id_cliente, fecha, total, estado) VALUES
('FAC-001', 1, '2026-09-16', 12.50, 'Pagado'),
('FAC-002', 2, '2026-09-17', 25.00, 'Pagado'),
('FAC-003', 3, '2026-09-18', 18.00, 'Pendiente'),
('FAC-004', 4, '2026-09-19', 30.50, 'Pagado'),
('FAC-005', 5, '2026-09-20', 15.00, 'Pendiente');
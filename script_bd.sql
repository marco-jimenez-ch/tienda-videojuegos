-- ============================================================
--  Creación de tablas para la tienda de videojuegos
-- ============================================================

-- ── TABLA: DN_ROL ────────────────────────────────────────────
CREATE TABLE DN_ROL (
    id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre      VARCHAR2(50)  NOT NULL,
    descripcion VARCHAR2(200) DEFAULT '',
    CONSTRAINT uq_rol_nombre UNIQUE (nombre)
);

-- ── TABLA: DN_PERFIL ─────────────────────────────────────────
CREATE TABLE DN_PERFIL (
    id               NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    usuario_id       NUMBER        NOT NULL,
    rol_id           NUMBER,
    nombre_completo  VARCHAR2(150) NOT NULL,
    fecha_nacimiento DATE,
    direccion        VARCHAR2(255) DEFAULT '',
    fecha_registro   TIMESTAMP     NOT NULL,
    CONSTRAINT uq_perfil_usuario UNIQUE (usuario_id),
    CONSTRAINT fk_perfil_usuario FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_perfil_rol     FOREIGN KEY (rol_id)     REFERENCES DN_ROL(id)    ON DELETE SET NULL
);

-- ── TABLA: DN_CATEGORIA ──────────────────────────────────────
CREATE TABLE DN_CATEGORIA (
    id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre      VARCHAR2(50)  NOT NULL,
    descripcion VARCHAR2(200) DEFAULT '',
    CONSTRAINT uq_categoria_nombre UNIQUE (nombre)
);

-- ── TABLA: DN_PRODUCTO ───────────────────────────────────────
CREATE TABLE DN_PRODUCTO (
    id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    categoria_id NUMBER,
    nombre      VARCHAR2(150) NOT NULL,
    descripcion CLOB          DEFAULT '',
    precio      NUMBER(10)    DEFAULT 0  NOT NULL,
    stock       NUMBER(6)     DEFAULT 0  NOT NULL,
    imagen      VARCHAR2(100) DEFAULT '',
    plataforma  VARCHAR2(100) DEFAULT '',
    activo      NUMBER(1)     DEFAULT 1  NOT NULL,
    CONSTRAINT fk_producto_categoria FOREIGN KEY (categoria_id) REFERENCES DN_CATEGORIA(id) ON DELETE SET NULL
);

-- ── TABLA: DN_CARRITO ─────────────────────────────────────────
CREATE TABLE DN_CARRITO (
    id             NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    usuario_id     NUMBER    NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL,
    activo         NUMBER(1) DEFAULT 1 NOT NULL,
    CONSTRAINT fk_carrito_usuario FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- ── TABLA: DN_DETALLE_CARRITO ────────────────────────────────
CREATE TABLE DN_DETALLE_CARRITO (
    id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    carrito_id      NUMBER    NOT NULL,
    producto_id     NUMBER    NOT NULL,
    cantidad        NUMBER(4) DEFAULT 1  NOT NULL,
    precio_unitario NUMBER(10) DEFAULT 0 NOT NULL,
    CONSTRAINT fk_detalle_carrito  FOREIGN KEY (carrito_id)  REFERENCES DN_CARRITO(id)  ON DELETE CASCADE,
    CONSTRAINT fk_detalle_producto FOREIGN KEY (producto_id) REFERENCES DN_PRODUCTO(id) ON DELETE CASCADE
);

COMMIT;

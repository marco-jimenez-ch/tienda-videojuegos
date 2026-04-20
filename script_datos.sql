-- ============================================================
--  Descripción: Inserción de datos base para la tienda de videojuegos
-- ============================================================

-- ── ROLES ────────────────────────────────────────────────────
INSERT INTO DN_ROL (nombre, descripcion)
    VALUES ('administrador', 'Administrador con acceso completo a la aplicacion');
INSERT INTO DN_ROL (nombre, descripcion)
    VALUES ('usuario', 'Usuario estandar de la tienda');

-- ── CATEGORÍAS ───────────────────────────────────────────────
INSERT INTO DN_CATEGORIA (nombre, descripcion)
    VALUES ('Accion', 'Combates intensos y adrenalina pura');
INSERT INTO DN_CATEGORIA (nombre, descripcion)
    VALUES ('Aventura', 'Historias profundas y mundos enormes');
INSERT INTO DN_CATEGORIA (nombre, descripcion)
    VALUES ('FPS', 'Accion en primera persona');
INSERT INTO DN_CATEGORIA (nombre, descripcion)
    VALUES ('Deportes', 'Competencia, estrategia y superacion');
INSERT INTO DN_CATEGORIA (nombre, descripcion)
    VALUES ('RPG', 'Crea tu personaje y construye tu historia');

-- ── PRODUCTOS ─────────────────────────────────────────────────
-- Acción (categoria_id = 1)
INSERT INTO DN_PRODUCTO (categoria_id, nombre, descripcion, precio, stock, imagen, plataforma, activo)
    VALUES (1, 'Devil May Cry 5', 'Hack and slash frenetico con combos espectaculares y protagonistas carismaticos.', 19990, 12, 'accion-1.jpg', 'PC - PS5 - Xbox', 1);
INSERT INTO DN_PRODUCTO (categoria_id, nombre, descripcion, precio, stock, imagen, plataforma, activo)
    VALUES (1, 'Bayonetta 3', 'Accion exagerada, poderes magicos y enemigos gigantes.', 22990, 8, 'accion-2.jpg', 'Nintendo Switch', 1);

-- Aventura (categoria_id = 2)
INSERT INTO DN_PRODUCTO (categoria_id, nombre, descripcion, precio, stock, imagen, plataforma, activo)
    VALUES (2, 'Zelda Tears of the Kingdom', 'Explora Hyrule con libertad total y descubre sus secretos.', 39990, 15, 'aventura-1.jpg', 'Nintendo Switch', 1);
INSERT INTO DN_PRODUCTO (categoria_id, nombre, descripcion, precio, stock, imagen, plataforma, activo)
    VALUES (2, 'Hollow Knight', 'Metroidvania oscuro ambientado en un reino de insectos subterraneo.', 9990, 30, 'aventura-2.jpg', 'PC - PS4 - Xbox - Switch', 1);

-- FPS (categoria_id = 3)
INSERT INTO DN_PRODUCTO (categoria_id, nombre, descripcion, precio, stock, imagen, plataforma, activo)
    VALUES (3, 'Doom Eternal', 'Elimina hordas de demonios a velocidad brutal.', 24990, 20, 'fps-1.jpg', 'PC - PS5 - Xbox - Switch', 1);
INSERT INTO DN_PRODUCTO (categoria_id, nombre, descripcion, precio, stock, imagen, plataforma, activo)
    VALUES (3, 'Halo Infinite', 'El Master Chief regresa en una aventura de mundo abierto.', 29990, 10, 'fps-2.jpg', 'PC - Xbox', 1);

-- Deportes (categoria_id = 4)
INSERT INTO DN_PRODUCTO (categoria_id, nombre, descripcion, precio, stock, imagen, plataforma, activo)
    VALUES (4, 'EA Sports FC 26', 'El futbol mas realista con licencias oficiales.', 34990, 25, 'deportes-1.jpg', 'PC - PS5 - Xbox - Switch', 1);
INSERT INTO DN_PRODUCTO (categoria_id, nombre, descripcion, precio, stock, imagen, plataforma, activo)
    VALUES (4, 'NBA 2K26', 'Baloncesto de alto nivel con el modo MyCareer mas inmersivo.', 32990, 18, 'deportes-2.jpg', 'PC - PS5 - Xbox', 1);

-- RPG (categoria_id = 5)
INSERT INTO DN_PRODUCTO (categoria_id, nombre, descripcion, precio, stock, imagen, plataforma, activo)
    VALUES (5, 'Elden Ring', 'RPG de mundo abierto oscuro creado por FromSoftware.', 39990, 14, 'rpg-1.jpg', 'PC - PS5 - Xbox', 1);
INSERT INTO DN_PRODUCTO (categoria_id, nombre, descripcion, precio, stock, imagen, plataforma, activo)
    VALUES (5, 'Baldurs Gate 3', 'RPG por turnos basado en DD con narrativa profunda.', 44990, 9, 'rpg-2.jpg', 'PC - PS5', 1);

COMMIT;

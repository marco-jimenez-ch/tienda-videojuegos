from core.models import Categoria, Producto

cats = {
    'Accion':    'Combates intensos y adrenalina pura.',
    'Aventura':  'Historias profundas y mundos enormes.',
    'FPS':       'Accion en primera persona.',
    'Deportes':  'Competencia y superacion.',
    'RPG':       'Crea tu personaje y construye tu historia.',
}

cat_objs = {}
for nombre, desc in cats.items():
    c, _ = Categoria.objects.get_or_create(
        nombre=nombre,
        defaults={'descripcion': desc}
    )
    cat_objs[nombre] = c

productos = [
    ('Devil May Cry 5', 'Hack and slash frenetico con combos espectaculares.', 19990, 12, 'accion-1.jpg', 'PC - PS5 - Xbox', 'Accion'),
    ('Bayonetta 3', 'Accion exagerada, poderes magicos y enemigos gigantes.', 22990, 8, 'accion-2.jpg', 'Nintendo Switch', 'Accion'),
    ('Zelda Tears of the Kingdom', 'Explora Hyrule con libertad total.', 39990, 15, 'aventura-1.jpg', 'Nintendo Switch', 'Aventura'),
    ('Hollow Knight', 'Metroidvania oscuro ambientado en un reino subterraneo.', 9990, 30, 'aventura-2.jpg', 'PC - PS4 - Xbox - Switch', 'Aventura'),
    ('Doom Eternal', 'Elimina hordas de demonios a velocidad brutal.', 24990, 20, 'fps-1.jpg', 'PC - PS5 - Xbox - Switch', 'FPS'),
    ('Halo Infinite', 'El Master Chief regresa en una aventura de mundo abierto.', 29990, 10, 'fps-2.jpg', 'PC - Xbox', 'FPS'),
    ('EA Sports FC 26', 'El futbol mas realista con licencias oficiales.', 34990, 25, 'deportes-1.jpg', 'PC - PS5 - Xbox - Switch', 'Deportes'),
    ('NBA 2K26', 'Baloncesto de alto nivel con el modo MyCareer mas inmersivo.', 32990, 18, 'deportes-2.jpg', 'PC - PS5 - Xbox', 'Deportes'),
    ('Elden Ring', 'RPG de mundo abierto oscuro creado por FromSoftware.', 39990, 14, 'rpg-1.jpg', 'PC - PS5 - Xbox', 'RPG'),
    ('Baldurs Gate 3', 'RPG por turnos basado en DD con narrativa profunda.', 44990, 9, 'rpg-2.jpg', 'PC - PS5', 'RPG'),
]

for nombre, desc, precio, stock, imagen, plataforma, cat_nombre in productos:
    Producto.objects.get_or_create(
        nombre=nombre,
        defaults={
            'descripcion': desc,
            'precio': precio,
            'stock': stock,
            'imagen': imagen,
            'plataforma': plataforma,
            'categoria': cat_objs[cat_nombre],
        }
    )

print("Categorias creadas: " + str(Categoria.objects.count()))
print("Productos creados: " + str(Producto.objects.count()))

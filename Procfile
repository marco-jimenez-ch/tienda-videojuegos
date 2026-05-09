web: python manage.py collectstatic --noinput && python manage.py migrate --noinput && gunicorn tienda_videojuegos.wsgi:application --bind 0.0.0.0:$PORT

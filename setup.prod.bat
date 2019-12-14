docker-compose -f docker-compose.prod.yaml exec django python manage.py collectstatic --no-input
docker-compose -f docker-compose.prod.yaml exec django python manage.py flush --no-input
docker-compose -f docker-compose.prod.yaml exec django python manage.py migrate --no-input
docker-compose -f docker-compose.prod.yaml exec django python manage.py createsuperuser

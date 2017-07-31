python manage.py migrate
python manage.py collectstatic --no-input
gunicorn peachpayments.wsgi:application -b :80 --reload

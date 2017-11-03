import os

SLACK_CHANNEL = 'transactions'

PEACH_USER_ID = os.environ.get('PEACH_USER_ID')
PEACH_PASSWORD = os.environ.get('PEACH_PASSWORD')
PEACH_ENTITY_ID = os.environ.get('PEACH_ENTITY_ID')
PEACH_RESULT_PAGE = os.environ.get('PEACH_RESULT_PAGE')
PEACH_ENTITY_RECURRING_ID = os.environ.get('PEACH_ENTITY_RECURRING_ID')
PEACH_BASE_URL = os.environ.get('PEACH_BASE_URL')

ALLOWED_HOSTS = [host.strip() for host in os.environ.get("ALLOWED_HOSTS", '').split(',')]

# aws storage
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = True
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = 'eu-central-1'
# AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)
STATIC_URL = "https://s3.amazonaws.com/{}/".format(AWS_STORAGE_BUCKET_NAME)
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# database:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', 'postgres'),
        'USER': os.environ.get('DATABASE_USER', 'postgres'),
        'HOST': os.environ.get('DATABASE_HOST', 'db'),
        'PORT': 5432,
    }
}
db_password = os.environ.get('DATABASE_PASSWORD', False)
if db_password:
    DATABASES.get('default').update({'PASSWORD': db_password})

COMMUNICATIONGURU_URL = 'https://communicationguru.appointmentguru.co'
DEFAULT_FROM_EMAIL = 'support@appointmentguru.co'

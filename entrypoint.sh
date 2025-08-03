#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
from finance_app.models import UserProfile

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    UserProfile.objects.get_or_create(user=user, defaults={'display_name': '系统管理员'})
    print("Superuser created: admin/admin123")
else:
    print("Superuser already exists")
EOF

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn finance_project.wsgi:application \
--bind 0.0.0.0:8000 \
--workers 3 \
--timeout 120 \
--keep-alive 2 \
--max-requests 1000 \
--max-requests-jitter 100 \
--access-logfile - \
--error-logfile - \
--max-requests-jitter 100 \
--access-logfile - \
--error-logfile -

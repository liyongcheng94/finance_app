#!/bin/bash

# Wait for database to be ready if using PostgreSQL
if [[ "$DATABASE_URL" == *"postgres"* ]]; then
    echo "Waiting for PostgreSQL..."
    while ! nc -z db 5432; do
        sleep 0.1
    done
    echo "PostgreSQL is ready!"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating development superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
from finance_app.models import UserProfile

User = get_user_model()
if not User.objects.filter(username='dev').exists():
    user = User.objects.create_superuser('dev', 'dev@example.com', 'dev123')
    UserProfile.objects.get_or_create(user=user, defaults={'display_name': '开发用户'})
    print("Development superuser created: dev/dev123")
else:
    print("Development superuser already exists")
EOF

# Start Django development server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000

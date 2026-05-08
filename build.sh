#!/bin/bash
set -e

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python CRM01/manage.py collectstatic --noinput

# Run database migrations
echo "🗄️  Running database migrations..."
python CRM01/manage.py migrate

# Create superuser if not exists (optional, for demo)
echo "👤 Creating admin user if not exists..."
python CRM01/manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created successfully!')
else:
    print('ℹ️  Superuser already exists.')
EOF

echo "✅ Build completed successfully!"

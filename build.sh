#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create necessary directories if they don't exist
mkdir -p staticfiles
mkdir -p media

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate 
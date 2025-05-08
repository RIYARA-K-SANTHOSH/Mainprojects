# Fixing Static Files Issues on Render

This guide will help you troubleshoot and fix static file issues when deploying Django applications to Render.

## Common Issues

1. **Static files not loading**: CSS, JavaScript, or images not appearing on your website after deployment
2. **404 errors on static resources**: Static files return 404 Not Found errors when accessed directly
3. **Broken styles/layouts**: Website appears without styling or with broken layouts due to missing static files

## Solution Steps

Follow these steps sequentially to fix static file issues:

### 1. Configure WhiteNoise for Static File Serving

WhiteNoise is a simple solution for serving static files in production without needing a separate web server like Nginx.

**Install WhiteNoise:**
```bash
pip install whitenoise
```

**Add to requirements.txt:**
```
whitenoise==6.6.0
```

**Update settings.py:**

```python
INSTALLED_APPS = [
    # ... other apps
    'django.contrib.staticfiles',
    'matrimonyapp',
    'whitenoise.runserver_nostatic',  # Add this line
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line right after security middleware
    # ... other middleware
]

# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "matrimonyapp/static"),  # Adjust to your app name
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 2. Ensure Static Directories Exist

Create any necessary directories for static file collection:

```bash
mkdir -p staticfiles
mkdir -p media
```

### 3. Collect Static Files

Make sure to run the collectstatic command in your build process:

```bash
python manage.py collectstatic --noinput
```

This should be included in your `build.sh` script:

```bash
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
```

### 4. Check Template References

Make sure all your templates reference static files correctly. Use the `{% load static %}` tag and reference files with the `{% static 'path/to/file' %}` template tag:

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
<body>
    <img src="{% static 'images/logo.png' %}">
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>
```

### 5. Configure Database URL for Render

For better database connection handling:

```python
import dj_database_url

# Check for DATABASE_URL env var to support Render deployment
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Your default database configuration
```

And add to requirements.txt:
```
dj-database-url==2.1.0
```

### 6. Add Render-Specific Configuration

Make sure to allow your Render domain in your settings:

```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Add render.com domain to allowed hosts
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
```

### 7. Create a Procfile

Create a Procfile in your project root with:

```
web: gunicorn connect.wsgi
```

### 8. Environment Variables on Render

Set these key environment variables in the Render dashboard:
- `DEBUG`: Set to `False` for production
- `SECRET_KEY`: Your secret key
- `ALLOWED_HOSTS`: List your allowed hosts, comma-separated
- `DATABASE_URL`: Will be set automatically if using Render's database service

## Troubleshooting

If you're still experiencing issues:

1. **Check the build logs**: Ensure collectstatic ran successfully
2. **Verify file paths**: Make sure your template references match your actual file structure
3. **Inspect browser console**: Look for 404 errors on specific static files
4. **Test locally**: Run with DEBUG=False locally to test production static file serving
5. **Check app structure**: Ensure your static files are in the correct directories
6. **Validate settings**: Double-check all your static file settings

## Verification

Run this check script to verify your static configuration locally:

```python
python check_static_config.py
```

This will help identify any misconfigurations before deployment.

## Need More Help?

If these steps don't resolve your issue:
- Check your template paths against the actual file paths
- Verify the Render service is properly configured
- Consider opening a support ticket with Render if the issue persists 
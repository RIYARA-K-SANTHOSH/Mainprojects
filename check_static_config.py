#!/usr/bin/env python
"""
Static Files Configuration Check Script

This script checks your Django settings to verify that static files 
are configured correctly for deployment on Render.
"""

import os
import sys
import importlib.util
from pathlib import Path

# Add the project's base directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Import the settings module
try:
    spec = importlib.util.spec_from_file_location("settings", "connect/settings.py")
    settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings)
    print("✅ Successfully loaded settings module")
except Exception as e:
    print(f"❌ Error loading settings module: {e}")
    sys.exit(1)

# Check for essential static files settings
checks = {
    "STATIC_URL": getattr(settings, "STATIC_URL", None),
    "STATIC_ROOT": getattr(settings, "STATIC_ROOT", None),
    "STATICFILES_DIRS": getattr(settings, "STATICFILES_DIRS", None),
    "STATICFILES_STORAGE": getattr(settings, "STATICFILES_STORAGE", None),
}

print("\n--- Static Files Configuration Check ---")

for setting_name, setting_value in checks.items():
    if setting_value:
        print(f"✅ {setting_name} is set to: {setting_value}")
    else:
        print(f"❌ {setting_name} is not set!")

# Check if WhiteNoise middleware is correctly configured
middlewares = getattr(settings, "MIDDLEWARE", [])
whitenoise_middleware = "whitenoise.middleware.WhiteNoiseMiddleware"

if whitenoise_middleware in middlewares:
    position = middlewares.index(whitenoise_middleware)
    print(f"✅ WhiteNoise middleware is configured (position {position})")
    
    # Check if positioned correctly (after SecurityMiddleware)
    security_middleware = "django.middleware.security.SecurityMiddleware"
    if security_middleware in middlewares:
        security_position = middlewares.index(security_middleware)
        if security_position < position:
            print("✅ WhiteNoise middleware is correctly positioned after SecurityMiddleware")
        else:
            print("⚠️ WhiteNoise middleware should come after SecurityMiddleware")
else:
    print("❌ WhiteNoise middleware is not configured!")

# Check if whitenoise is in INSTALLED_APPS
installed_apps = getattr(settings, "INSTALLED_APPS", [])
whitenoise_app = "whitenoise.runserver_nostatic"
if whitenoise_app in installed_apps:
    print("✅ whitenoise.runserver_nostatic is in INSTALLED_APPS")
else:
    print("⚠️ Consider adding 'whitenoise.runserver_nostatic' to INSTALLED_APPS")

# Check if directories exist
static_root = getattr(settings, "STATIC_ROOT", None)
if static_root and os.path.exists(static_root):
    print(f"✅ STATIC_ROOT directory exists at {static_root}")
else:
    print(f"⚠️ STATIC_ROOT directory does not exist at {static_root}")

print("\n--- Directory Check ---")
staticfiles_dirs = getattr(settings, "STATICFILES_DIRS", [])
for directory in staticfiles_dirs:
    if os.path.exists(directory):
        print(f"✅ Directory exists: {directory}")
        # Check if directory contains files
        files = list(Path(directory).rglob("*"))
        if files:
            print(f"   - Contains {len(files)} files/directories")
        else:
            print("   - ⚠️ Directory is empty!")
    else:
        print(f"❌ Directory does not exist: {directory}")

print("\nRun this command to verify static files collection:")
print(f"python manage.py collectstatic --dry-run --noinput")
print("\nIf all looks good, run without --dry-run to actually collect the files.") 
# Connect Matrimony App

A Django-based matrimony application with ML features for profile matching and analysis.

## Deployment Guide for Render

### Prerequisites

- GitHub repository with your code
- Render account (free tier available)
- Database service (MySQL recommended for production)

### Steps to Deploy on Render

1. **Create a Web Service on Render**

   - Sign in to your Render account
   - Click "New" and select "Web Service"
   - Connect your GitHub repository
   - Use the following settings:
     - Name: `connect-matrimony` (or your preferred name)
     - Runtime: `Python 3`
     - Build Command: `./build.sh`
     - Start Command: `gunicorn connect.wsgi`
     - Select the appropriate instance type (free tier is okay for testing)

2. **Set Environment Variables**

   In the Render dashboard for your web service, go to "Environment" and add the environment variables listed in the `env.example` file. Make sure to update them with your actual values.

   **IMPORTANT:** For Render, it's recommended to use the `DATABASE_URL` environment variable instead of individual database settings.

3. **Database Setup**

   - For production, use a MySQL database (you can use Render's database service or an external one)
   - For the free tier, you can use SQLite for testing, but it's not recommended for production
   - If using Render's database service, copy the `External Database URL` and set it as `DATABASE_URL` environment variable

4. **Static Files Configuration**

   The application is configured to use WhiteNoise for serving static files. This is already set up in the settings.py file. The build.sh script will:
   - Create necessary directories
   - Run collectstatic to gather all static files into the staticfiles directory
   - WhiteNoise will serve these files efficiently in production

   **Troubleshooting Static Files:**
   - If static files aren't loading, make sure the `STATIC_URL` and `STATIC_ROOT` settings are correct
   - Check that `whitenoise.middleware.WhiteNoiseMiddleware` is in your MIDDLEWARE settings
   - Verify that the static files were collected during the build process (check build logs)
   - Make sure there are no errors in your HTML templates referencing static files

5. **Initial Setup**

   The `build.sh` script will automatically:
   - Install dependencies from requirements.txt
   - Create necessary directories
   - Collect static files
   - Run database migrations

### Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Copy `env.example` to `.env` and update with your values
5. Install dependencies: `pip install -r requirements.txt`
6. Run migrations: `python manage.py migrate`
7. Start the server: `python manage.py runserver`

## Features

- User registration and profile creation
- Profile matching with ML-based recommendations
- Image analysis with gender detection
- Payment processing with Razorpay
- Comprehensive search and filtering

## ML Optimization

The ML components use lazy loading to optimize resource usage:
- Models are only loaded when needed
- Dependencies like TensorFlow, OpenCV, and scikit-learn are imported just when required
- Improved memory efficiency for production environments 
# Munarchy Backend

The backend repository for Munarchy'25 - IIT Roorkee's flagship MUN event.

## 🛠 Tech Stack

- **Framework:** Quart
- **Database:** MongoDB
- **Email Service:** SMTP
- **Deployment:** Docker & Docker Compose
- **ASGI Server:** Gunicorn with Uvicorn workers

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- MongoDB instance

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/baync180705/munarchy_backend.git
   cd munarchy-backend
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server**
   ```bash
   gunicorn app:app -c gunicorn_config.py
   ```

### Docker Setup

1. **Build and run using Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or run individual commands**
   ```bash
   # Build the image
   sudo docker build -t munarchy-backend .

   # Run the container
   sudo docker run -p 8000:8000 munarchy-backend
   ```

## 📁 Project Structure

- **src/api/routes/**: API routes for user registration and management.
- **src/models/**: Data models for the application.
- **src/services/**: Business logic and services for the application.
- **src/utils/**: Utility functions and helpers.
- **src/config/**: Configuration settings for the application.
- **src/core/**: Core functionality and database operations.
- **src/tests/**: Test cases for the application.
- **src/main.py**: Entry point for the application.

## ⚙️ Environment Variables

Create a `.env` file in the root directory with the following variables:
- MERCHANT_KEY
- SALT
- ENV
- MONGO_URI
- SENDER_EMAIL
- EMAIL_SECRET_KEY
- SURL
- FURL
- BASE_URL
- SSL_KEYFILE
- SSL_CERTFILE

## 📦 Deployment

The application is containerized and can be deployed using Docker. The included Docker configuration handles all dependencies and environment setup.
# AyuVibe Backend

AyuVibe is an Ayurvedic medicine application backend built with **FastAPI** and **PostgreSQL**. It provides functionalities such as user authentication, a doctor directory, herbal remedies database, and an Ayurvedic chatbot.

## Features

- **User Authentication**: Secure login and signup functionalities using JWT.
- **Doctor Directory**: Browse and search for Ayurvedic doctors.
- **Herbal Remedies**: Comprehensive database of herbs and their uses.
- **Ayurvedic Chatbot**: Interactive chatbot for Ayurvedic consultations.
- **API Documentation**: Automatically generated with Swagger UI.
- **Deployment Ready**: Containerized with Docker and deployable on Kubernetes.

## Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger UI (built-in with FastAPI)
- **Deployment**: Docker & Kubernetes

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Docker](#docker)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Ensure you have the following installed on your machine:

- **Python**: Version 3.8 or above. [Download Python](https://www.python.org/downloads/)
- **PostgreSQL**: Version 12 or above. [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git**: For cloning the repository. [Download Git](https://git-scm.com/downloads)
- **Docker** (optional): For containerized deployments. [Download Docker](https://www.docker.com/get-started)
- **Docker Compose** (optional): For managing multi-container Docker applications. [Install Docker Compose](https://docs.docker.com/compose/install/)

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Deshmukh1992/ayuvibe-backend.git
    cd ayuvibe-backend
    ```

2. **Set Up a Virtual Environment**

    It's recommended to use a virtual environment to manage dependencies.

    ```bash
    python -m venv venv
    ```

    Activate the virtual environment:

    - On **Unix or MacOS**:

        ```bash
        source venv/bin/activate
        ```

    - On **Windows**:

        ```bash
        venv\Scripts\activate
        ```

3. **Install Dependencies**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the root directory of the project and add the following environment variables:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/ayuvibe_db

# JWT Configuration
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```


# AyuVibe Backend

AyuVibe is an Ayurvedic medicine application backend that provides functionalities such as user login, a doctor directory, herbs and remedies database, and a chatbot related to Ayurveda.

## Features

- User authentication (login/signup)
- Doctor directory with search and filter capabilities
- Herbal remedies and treatments database
- Ayurvedic chatbot support
- API integrations with the frontend

## Tech Stack

- **Backend Framework**: Node.js with Express
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger
- **Deployment**: Kubernetes (MLflow integrated)

## Getting Started

These instructions will help you set up the backend server for development and testing purposes.

### Prerequisites

- **Node.js**: Ensure Node.js is installed on your machine. You can download it from [Node.js Official Site](https://nodejs.org/).
- **MongoDB**: Make sure you have MongoDB running either locally or in the cloud (e.g., MongoDB Atlas).
- **Docker** (optional): For containerized deployments.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Deshmukh1992/ayuvibe-backend.git
    cd ayuvibe-backend
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Create a `.env` file in the root of the project and add the following environment variables:

    ```env
    PORT=5000
    MONGO_URI=mongodb://localhost:27017/ayuvibe
    JWT_SECRET=your_jwt_secret
    ```

4. Start the development server:

    ```bash
    npm run dev
    ```

    The server will start at `http://localhost:5000`.

### API Endpoints

| Endpoint              | Method | Description                            |
|-----------------------|--------|----------------------------------------|
| `/api/users/register`  | POST   | Register a new user                    |
| `/api/users/login`     | POST   | User login                             |
| `/api/doctors`         | GET    | Get list of doctors                    |
| `/api/herbs`           | GET    | Get list of herbs and remedies         |
| `/api/chatbot`         | POST   | Interact with the Ayurvedic chatbot    |

### Testing

To run tests, use the following command:

```bash
npm test

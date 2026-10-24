# 3-Tier Architecture — Claims Management Application

A three-tier Claims Management Application built using React, Flask, and PostgreSQL. This project is used to practise application development and DevOps workflows, including running the application locally with Docker Compose.

## Architecture

```text
                  CLAIMS MANAGEMENT APPLICATION
                       3-TIER ARCHITECTURE

                             USER
                               |
                               v
                 +-------------------------+
                 | TIER 1: PRESENTATION    |
                 | React + Nginx           |
                 | localhost:8081          |
                 +------------+------------+
                              |
                         REST API / JSON
                              |
                              v
                 +-------------------------+
                 | TIER 2: APPLICATION     |
                 | Flask + Gunicorn        |
                 | localhost:5001          |
                 +------------+------------+
                              |
                          SQL / DB
                              |
                              v
                 +-------------------------+
                 | TIER 3: DATA            |
                 | PostgreSQL              |
                 | Database: claimsdb      |
                 | Internal port: 5432     |
                 +-------------------------+
```

Docker Compose manages the frontend, backend, and database as separate services on a private network. The frontend communicates with the backend through HTTP REST APIs, and the backend communicates with PostgreSQL to store and retrieve application data.

## Project Structure

```text
3-Tier-Architecture/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── nginx.conf
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   └── Dockerfile
├── database/
│   └── init.sql
├── usecase-03/
│   └── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

The project structure above describes the expected files for the local Docker Compose setup. The exact files may vary depending on the current implementation.

## Technologies Used

- **React and Vite:** Frontend development
- **Flask and Python:** Backend REST API
- **Gunicorn:** Backend application server
- **PostgreSQL:** Relational database
- **Docker:** Container images and runtime
- **Docker Compose:** Local multi-service orchestration
- **Nginx:** Frontend web server and API reverse proxy
- **Git and GitHub:** Version control
- **curl:** API and HTTP testing

## Application Features

- User registration and login APIs
- Claims creation and retrieval
- Claims update functionality
- Automatic claim number generation
- PostgreSQL-backed data storage
- Health-check endpoint for backend verification
- Containerized frontend, backend, and database services

## Backend API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Check backend health |
| GET | `/api/claims` | Retrieve claims |
| POST | `/api/claims` | Create a claim |
| PUT | `/api/claims/<id>` | Update a claim |
| POST | `/api/register` | Register a user |
| POST | `/api/login` | Authenticate a user |

## Use Case 03 — Run the App Locally and Prepare Config

### Objective

Run the complete Claims Management Application locally using Docker Compose, configure services through environment variables, protect credentials, and verify application functionality and database persistence.

### Configuration and Security

- `.env.example` provides a template for the required environment variables.
- `.env` stores local configuration and credentials and must not be committed to Git.
- `.gitignore` excludes private environment files and other files that should not be tracked.
- Docker Compose supplies the configuration required by the frontend, backend, and database.
- Environment variables allow the backend to connect to PostgreSQL without hardcoding local credentials into the application.
- A named Docker volume stores PostgreSQL data independently of the database container lifecycle.

### Local Application URLs

| Component | URL or Port |
|---|---|
| Frontend | http://localhost:8081 |
| Backend health endpoint | http://localhost:5001/api/health |
| Backend claims endpoint | http://localhost:5001/api/claims |
| PostgreSQL internal port | `5432` |

The PostgreSQL service is accessed by the backend over the internal Docker Compose network. The frontend accesses the backend through the configured HTTP API route.

### Implementation Workflow

1. Review the existing frontend, backend, database initialization script, and Dockerfiles.
2. Prepare `.env.example` and the local `.env` configuration.
3. Configure `.gitignore` to prevent private credentials from being committed.
4. Define the frontend, backend, and PostgreSQL services in `docker-compose.yml`.
5. Configure the application services, ports, environment variables, health checks, and database volume as required.
6. Validate the Compose configuration.
7. Build the required container images and start the services.
8. Verify service health, frontend access, backend APIs, and database connectivity.
9. Test frontend-to-backend-to-database communication by creating and retrieving a claim.
10. Review container logs and runtime status to identify errors.
11. Simulate a database outage, restore the database service, and verify application recovery.
12. Restart the Compose stack and confirm that previously stored claims remain available.
13. Update the project documentation with the commands, configuration, verification steps
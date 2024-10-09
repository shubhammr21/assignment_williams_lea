# README for Django Project

## Project Overview

This Django application fetches XML data from [UK Legislation](https://www.legislation.gov.uk/uksi/2024/979/contents/made/data.xml) and renders it in a format similar to the official webpage. The project includes:

- **Unit Testing** to ensure functionality.
- **SOLID Principles** for clean, maintainable code.
- **Web Accessibility** following [W3C standards](https://www.w3.org/WAI/fundamentals/accessibility-intro/) to ensure usability for all users.

This project demonstrates best practices in both software design and accessibility.

## System Requirements

Before starting, ensure you have the following installed:

- **Python**: 3.12+
- **Docker**: 20.10+
- **Docker Compose**: (Follow the [installation guide](https://docs.docker.com/compose/install/))
- **Git**: 2.20+

## Getting Started with Docker

To set up and run the project using Docker, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/shubhammr21/assignment_williams_lea.git
cd assignment_williams_lea
```

### 2. Start the Docker Containers

To start the Django and PostgreSQL services using Docker Compose:

```bash
docker compose -f docker-compose.local.yml up
```

### 3. Access Django Shell

To access the Django container's shell:

```bash
docker compose -f docker-compose.local.yml exec -it django bash
```

You can now run any Django commands from within the container's bash environment.

### 4. Run Django Commands Directly

Alternatively, you can run Django commands directly from your terminal without accessing the shell:

```bash
docker compose -f docker-compose.local.yml exec -it django <your command>
```

For example, to check migrations:

```bash
docker compose -f docker-compose.local.yml exec -it django python manage.py makemigrations --check
```

### 5. Access the Application

Once the server is running, you can access the application in your browser at:

- **Docker**: `http://localhost:8000/`

---

## Common Docker Commands

- **Build the Stack**:

    ```bash
    docker compose -f docker-compose.local.yml build django
    ```

- **Check DB Migrations**:

    ```bash
    docker compose -f docker-compose.local.yml run --rm django python manage.py makemigrations --check
    ```

- **Run DB Migrations**:

    ```bash
    docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
    ```

- **Run Django Tests**:

    ```bash
    docker compose -f docker-compose.local.yml run django pytest
    ```

- **Tear Down the Stack**:

    ```bash
    docker compose -f docker-compose.local.yml down
    ```

---

## Running the Project Manually (Without Docker)

If you prefer to run the project locally without Docker, follow these steps:

### 1. Create a Virtual Environment

First, create a virtual environment for the project:

```bash
python3.12 -m venv .venv
```

### 2. Activate the Virtual Environment

- On **Linux/macOS**:

    ```bash
    source .venv/bin/activate
    ```

- On **Windows**:

    ```bash
    .venv\Scripts\activate
    ```

### 3. Install Dependencies

Install the necessary dependencies using the provided `requirements-dev.lock` file:

```bash
pip install -r requirements-dev.lock
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
DATABASE_URL=postgres://myuser:mypassword@localhost:5432/mydb
```

Ensure that PostgreSQL is installed and running if you are not using Docker for the database.

### 5. Run Database Migrations

Apply the database migrations:

```bash
python manage.py migrate
```

### 6. Start the Django Development Server

Finally, start the development server:

```bash
python manage.py runserver
```

### 7. Access the Application

Once the server is running, you can access the application in your browser at:

- **Local Setup**: `http://127.0.0.1:8000/`

---

## Additional Commands

### Create a Superuser

To create a Django superuser for accessing the admin panel:

```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
```

Or, if running locally:

```bash
python manage.py createsuperuser
```

### Collect Static Files

If you need to collect static files for production, use the following command:

```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py collectstatic
```

Or, if running locally:

```bash
python manage.py collectstatic
```

---

### Running in Production

To run the application in a production environment, use the following command:

```bash
docker compose -f docker-compose.production.yml up
```

This will configure the following services:

- **Django** for the application backend.
- **PostgreSQL** for the database.
- **Traefik** as the reverse proxy.
- **Nginx** to serve media files efficiently.

Ensure you have set up your environment variables for production in the `.env` file before running the command.

---

## Troubleshooting

- **Docker container fails to start**: Ensure Docker is running and check if any other services are using the ports (e.g., PostgreSQL on port 5432).
- **Database connection errors**: Double-check the `.env` file for correct PostgreSQL credentials and ensure the database service is running.
- **Permissions issues**: If you encounter permission issues, try running Docker with `sudo` or check your system's user permissions for Docker.

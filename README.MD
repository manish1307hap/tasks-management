# FastAPI Task Management API

This is a FastAPI project for managing tasks with full CRUD functionality. The project uses SQLAlchemy as ORM and supports SQLite/MySQL/PostgreSQL databases. It also includes proper dependency injection for services and supports migrations.

---

## Requirements

- Python 3.10+
- pip
- Virtual environment (optional but recommended)
- SQLite/MySQL/PostgresSQL (depending on configuration)
- Docker (for Approach 2)

---

## Project Setup

### Approach 1: Manual Setup

1. **Create a virtual environment**:

```bash
python3 -m venv venv
````

2. **Activate the virtual environment**:

```bash
source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run database migrations**:

If you are using Alembic:

```bash
alembic upgrade head
```

5. **Run the FastAPI application**:

```bash
uvicorn app.main:app --reload
```

---

### Approach 2: Dockerized Setup (`build_image.sh`)

A `build_image.sh` script is provided to build and run the application using Docker. This automates environment setup and containerization.

1. Make the script executable:

```bash
chmod +x build_image.sh
```

2. Run the script:

```bash
./build_image.sh
```

* This will:

  * Build the Docker image
  * Create and start a container with all dependencies
  * Run database migrations inside the container
  * Start the FastAPI server

> **Note:** Docker must be installed and running on your system.

---

## Running the Application

Once the server is running, you can access the API at:

```
http://127.0.0.1:8000
```

### API Documentation

FastAPI automatically provides Swagger UI and ReDoc:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Running Tests

To run the pytest test suite:

```bash
pytest
```

* Make sure your test database (e.g., SQLite in-memory or test DB) is configured properly.
* Tests cover all CRUD operations.

---

## API Endpoints

| Method | Path              | Description         |
| ------ | ----------------- | ------------------- |
| GET    | /tasks/health     | Health check        |
| GET    | /tasks/tasks      | List all tasks      |
| POST   | /tasks/tasks      | Create a new task   |
| GET    | /tasks/tasks/{id} | Get a task by ID    |
| PUT    | /tasks/tasks/{id} | Update a task by ID |
| DELETE | /tasks/tasks/{id} | Delete a task by ID |

```
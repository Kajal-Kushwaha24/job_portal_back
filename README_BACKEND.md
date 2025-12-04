# Job Portal Backend API

FastAPI backend for the Mini Job Portal App with MySQL database using SQLAlchemy ORM.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Update the `DATABASE_URL` in `database.py` or set it as an environment variable:

```bash
# Windows PowerShell
$env:DATABASE_URL="mysql+pymysql://root:password@localhost:3306/job_portal"

# Linux/Mac
export DATABASE_URL="mysql+pymysql://root:password@localhost:3306/job_portal"
```

**Database Configuration:**
- Replace `root` with your MySQL username
- Replace `password` with your MySQL password
- Replace `localhost:3306` with your MySQL host and port
- Replace `job_portal` with your database name

### 3. Create MySQL Database

```sql
CREATE DATABASE job_portal;
```

### 4. Initialize Database

Run the initialization script to create tables and default users:

```bash
python init_db.py
```

This will create:
- All database tables (users, jobs, applications)
- Default users:
  - `recruiter@test.com` / `123456` (recruiter)
  - `user@test.com` / `123456` (jobseeker)

### 5. Run the Server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### Authentication

**POST** `/login`
- Authenticates user and returns role
- Request body:
  ```json
  {
    "email": "recruiter@test.com",
    "password": "123456"
  }
  ```
- Response:
  ```json
  {
    "message": "Login successful",
    "role": "recruiter",
    "email": "recruiter@test.com"
  }
  ```

### Jobs

**GET** `/jobs`
- Returns list of all jobs
- Response: Array of job objects

**POST** `/jobs`
- Creates a new job (recruiter only)
- Request body:
  ```json
  {
    "title": "Software Engineer",
    "description": "We are looking for a software engineer...",
    "location": "New York",
    "recruiter_email": "recruiter@test.com"
  }
  ```
- Response:
  ```json
  {
    "message": "Job created successfully",
    "job_id": 1
  }
  ```

### Applications

**POST** `/apply`
- Apply for a job
- Request body:
  ```json
  {
    "user_email": "user@test.com",
    "job_id": 1
  }
  ```
- Response:
  ```json
  {
    "message": "Application submitted successfully",
    "application_id": 1
  }
  ```

## Database Schema

### users
- `id` (INT, PRIMARY KEY)
- `email` (VARCHAR(255), UNIQUE)
- `password` (VARCHAR(255))
- `role` (VARCHAR(50)) - 'recruiter' or 'jobseeker'

### jobs
- `id` (INT, PRIMARY KEY)
- `title` (VARCHAR(255))
- `description` (VARCHAR(2000))
- `location` (VARCHAR(255))
- `created_by` (INT, FOREIGN KEY -> users.id)
- `created_at` (DATETIME)

### applications
- `id` (INT, PRIMARY KEY)
- `user_email` (VARCHAR(255))
- `job_id` (INT, FOREIGN KEY -> jobs.id)

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


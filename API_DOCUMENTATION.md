# API Documentation

## Base URL
```
https://api-jd.vercel.app/api/v1
```

## Authentication
This API uses JWT for authentication. Include the token in the `Authorization` header:
```
Authorization: Bearer <your_token>
```

## Projects

### Get All Projects
```http
GET /projects
```

**Query Parameters:**
- `skill` (optional): Filter projects by skill (case-insensitive)
- `skip` (optional, default=0): Number of records to skip for pagination
- `limit` (optional, default=100, max=100): Maximum number of records to return

**Example Request:**
```bash
curl -X GET "https://api-jd.vercel.app/api/v1/projects?skill=python&skip=0&limit=10"
```

**Example Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "E-Commerce API",
    "description": "A RESTful API for an e-commerce platform built with FastAPI and PostgreSQL",
    "skills": ["python", "fastapi", "postgresql"],
    "github_url": "https://github.com/example/ecommerce-api",
    "demo_url": "https://api.example.com/ecommerce",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### Get Single Project
```http
GET /projects/{project_id}
```

**Path Parameters:**
- `project_id` (required): The ID of the project to retrieve

**Example Request:**
```bash
curl -X GET "https://api-jd.vercel.app/api/v1/projects/550e8400-e29b-41d4-a716-446655440000"
```

**Example Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "E-Commerce API",
  "description": "A RESTful API for an e-commerce platform built with FastAPI and PostgreSQL",
  "skills": ["python", "fastapi", "postgresql"],
  "github_url": "https://github.com/example/ecommerce-api",
  "demo_url": "https://api.example.com/ecommerce",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Create Project
```http
POST /projects
```

**Request Body:**
```json
{
  "title": "New Project",
  "description": "Project description",
  "skills": ["python", "fastapi"],
  "github_url": "https://github.com/example/new-project",
  "demo_url": "https://example.com/new-project"
}
```

**Example Request:**
```bash
curl -X POST "https://api-jd.vercel.app/api/v1/projects" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Project","description":"Project description","skills":["python","fastapi"],"github_url":"https://github.com/example/new-project","demo_url":"https://example.com/new-project"}'
```

**Example Response (201 Created):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "title": "New Project",
  "description": "Project description",
  "skills": ["python", "fastapi"],
  "github_url": "https://github.com/example/new-project",
  "demo_url": "https://example.com/new-project",
  "created_at": "2024-01-02T12:00:00",
  "updated_at": "2024-01-02T12:00:00"
}
```

### Update Project
```http
PUT /projects/{project_id}
```

**Path Parameters:**
- `project_id` (required): The ID of the project to update

**Request Body:** (Only include fields to update)
```json
{
  "title": "Updated Project Title",
  "skills": ["python", "fastapi", "mongodb"]
}
```

**Example Request:**
```bash
curl -X PUT "https://api-jd.vercel.app/api/v1/projects/660e8400-e29b-41d4-a716-446655440001" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Project Title","skills":["python","fastapi","mongodb"]}'
```

**Example Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "title": "Updated Project Title",
  "description": "Project description",
  "skills": ["python", "fastapi", "mongodb"],
  "github_url": "https://github.com/example/new-project",
  "demo_url": "https://example.com/new-project",
  "created_at": "2024-01-02T12:00:00",
  "updated_at": "2024-01-02T14:30:00"
}
```

### Delete Project
```http
DELETE /projects/{project_id}
```

**Path Parameters:**
- `project_id` (required): The ID of the project to delete

**Example Request:**
```bash
curl -X DELETE "https://api-jd.vercel.app/api/v1/projects/660e8400-e29b-41d4-a716-446655440001"
```

**Response:**
- 204 No Content (successful deletion)
- 404 Not Found (project not found)

## Environment Variables

### Backend
```
# Required
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://api-jd.vercel.app
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key

# Optional (with defaults)
ALLOWED_ORIGIN_REGEX=https?://(localhost|api-jd.*\.vercel\.app|api-jd\.onrender\.com)
PORT=8000
ENVIRONMENT=development
```

### Frontend
```
# Required
VITE_API_URL=https://api-jd.vercel.app/api/v1

# Optional
VITE_ENVIRONMENT=production
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message describing the issue"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

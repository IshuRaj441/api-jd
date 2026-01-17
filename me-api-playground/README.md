# Me-API Playground (Track A)

## Overview
A minimal backend + frontend project for the Track A assessment.
Demonstrates API design, database modeling, and deployment.

## Live URLs
- **Backend**: https://me-api-playground.onrender.com
- **Frontend**: https://me-api-playground.netlify.app

## Architecture
```
Frontend (React)
   ↓
Backend (FastAPI)
   ↓
SQLite Database
```

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: React, Vite
- **Deployment**: Render (Backend), Netlify (Frontend)

## API Endpoints

### Profile
- `GET /profile` - Get profile information
- `POST /profile` - Create profile
- `PUT /profile` - Update profile

### Projects
- `GET /projects` - List all projects
- `GET /projects?skill={skill}` - Filter projects by skill

### Skills
- `GET /skills/top` - Get top skills

### Search
- `GET /search?q={query}` - Search across projects and skills

### Health
- `GET /health` - Health check endpoint

## Database Schema
```
Profile
  - id: int (PK)
  - name: str
  - email: str
  - education: str
  - created_at: datetime
  - updated_at: datetime

Project
  - id: int (PK)
  - title: str
  - description: str
  - links: str
  - created_at: datetime
  - updated_at: datetime

Skill
  - id: int (PK)
  - name: str (unique)
  - created_at: datetime

ProjectSkill (association table)
  - project_id: int (FK to Project)
  - skill_id: int (FK to Skill)
```

## Database Seeding
The database is seeded using `seed.py` with real profile, skills, and project data.

## Design Notes
- SQLite used for simplicity and fast setup
- Minimal frontend by design (backend-focused assessment)
- No authentication implemented due to scope

## Trade-offs
- Used SQLite for development simplicity instead of a production-grade database
- Basic error handling without detailed error messages
- No rate limiting or request throttling
- No authentication/authorization layer

## Known Limitations
- No user authentication
- Limited input validation
- No pagination for large result sets
- No caching layer
- Search is case-sensitive

## Future Improvements
- Add authentication & authorization
- Implement pagination and caching
- Enhance input validation
- Add API versioning
- Add more comprehensive test coverage
- Implement rate limiting
- Add API documentation with Swagger/OpenAPI
- Add logging and monitoring
- Containerize the application with Docker

## Setup (Local)

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

4. Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

4. Run the frontend:
   ```bash
   npm run dev
   ```

## Setup (Production)

### Backend Deployment (Render)
1. Push code to GitHub repository
2. Create new Web Service on Render
3. Connect GitHub repository
4. Configure build and start commands:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Set environment variables in Render dashboard
6. Deploy

### Frontend Deployment (Netlify)
1. Push code to GitHub repository
2. Connect repository to Netlify
3. Set build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
4. Set environment variables in Netlify dashboard
5. Deploy

## Live URLs
- **Backend API**: [https://your-render-app.onrender.com](https://your-render-app.onrender.com)
- **Frontend**: [https://your-netlify-app.netlify.app](https://your-netlify-app.netlify.app)

## Resume
[Your Resume Link](https://drive.google.com/your-resume-link)

## Remarks
- The application demonstrates CRUD operations for a profile and projects
- Implements filtering and search functionality
- Follows RESTful API design principles
- Includes basic error handling and validation
- SQLite chosen for simplicity
- Minimal UI by design
- With more time, would add auth, pagination, and caching

### Search
- `GET /api/v1/search?q=query` - Search for projects and skills

## Setup

### Prerequisites
- Python 3.10+
- pip
- SQLite

### Backend Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python -c "from app.db.init_db import init_db, seed_db; init_db(); seed_db()"
   ```

4. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## Running Tests

```bash
cd backend
pytest -v
```

## Deployment

### Backend

The backend can be deployed using Docker:

```bash
docker build -t me-api-backend .
docker run -d -p 8000:8000 me-api-backend
```

### Frontend

Build the frontend for production:

```bash
cd frontend
npm run build
```

## Live URLs

- **Frontend**: [https://me-api-playground.vercel.app](https://me-api-playground.vercel.app)
- **Backend**: [https://me-api-backend.onrender.com](https://me-api-backend.onrender.com)

## Resume

[View my resume](https://drive.google.com/your-resume-link)

## Remarks

- Used SQLite for simplicity in development
- Minimal UI by design to focus on backend functionality
- Would add authentication, rate limiting, and caching in a production environment

Build and host a very basic playground that stores my own information (candidate profile) in a database and exposes it via a small API, plus a minimal frontend to run queries.

This repository is intentionally simple and focused on correctness, clarity, and reproducibility, as required by Track A.

🔗 Working URLs (Required)

Backend API (Hosted):
https://me-api-playground.onrender.com

Frontend UI (Hosted):
https://me-api-playground.netlify.app

Source Code Repository:
https://github.com/IshuRaj441/api-jd

1. Backend & API
Implemented Requirements

--> Exposes endpoints to create / read / update my profile
--> Supports query endpoints
--> Provides GET /health for liveness

Profile Data Model

The backend stores my real candidate data, including:

{
  "name": "",
  "email": "",
  "education": "",
  "skills": [],
  "projects": [
    {
      "title": "",
      "description": "",
      "links": []
    }
  ],
  "work": [],
  "links": {
    "github": "",
    "linkedin": "",
    "portfolio": ""
  }
}

API Endpoints
Health Check (Acceptance Criterion)
GET /health


✔ Returns 200 OK

Profile CRUD
GET    /profile
POST   /profile
PUT    /profile

Query Endpoints (Required)
GET /projects?skill=python
GET /skills/top
GET /search?q=fastapi


--> Queries return correct filtered results
--> Seeded data is visible through both API and UI

2. Database
Implementation

Database: SQLite

ORM: SQLAlchemy

Schema: Defined via SQLAlchemy models

Indexes: Applied on skills and project relationships

Schema Description

One profile

Skills stored as normalized records

Projects linked to skills (many-to-many)

All schema defined in code (no runtime inference)

Seed Data

--> Database is seeded with my real data on first run

3. Frontend (Very Basic)
Requirements Met

--> Plain React (Vite) UI
--> Search by skill
--> List projects
--> View profile
--> Calls hosted API
--> CORS configured correctly

The UI is intentionally minimal, per Track A instructions.

4. Hosting & Documentation
Deployment

Backend: Render

Frontend: Netlify

Both are publicly accessible and load without errors.

Local Setup (Reproducible)
Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload


Runs at:

http://127.0.0.1:8000

Frontend
cd frontend
npm install
npm run dev


Environment variable:

VITE_API_BASE_URL=http://127.0.0.1:8000

Production Configuration
Backend (Render)
uvicorn app.main:app --host 0.0.0.0 --port 8000

Frontend (Netlify)

Build command: npm run build

Publish directory: dist

VITE_API_BASE_URL=https://me-api-playground.onrender.com

5. API Testing
Postman Collection

--> Importable Postman collection included
--> Covers health, profile, and query endpoints
--> Uses environment variable for base URL

6. Known Limitations

No authentication (optional per Track A)

No pagination

SQLite used for simplicity

Minimal UI styling

Acceptance Criteria Checklist

--> GET /health returns 200
--> Queries return correct filtered results
--> Seed data visible via UI
--> README is complete and reproducible
--> URLs load without errors

Final Note

This project was implemented strictly against Track A requirements, prioritizing:

correctness

clarity

reproducibility

working deployments

Optional features were intentionally excluded.

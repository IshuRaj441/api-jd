# Me-API Playground - Frontend

This is the frontend for the Me-API Playground, a full-stack portfolio application built with React, Vite, and FastAPI. The application showcases professional profiles, projects, and skills in a modern, responsive interface.

## ✨ Features

- **Profile Management**
  - View and edit personal and professional information
  - Update social media links and contact details
  - Upload profile picture

- **Project Showcase**
  - Display projects with detailed descriptions
  - Filter projects by skills and technologies
  - Mark projects as featured
  - Include GitHub and live demo links

- **Search & Filter**
  - Full-text search across all content
  - Filter by skills, technologies, and project status
  - Pagination support for large result sets

- **Responsive Design**
  - Mobile-first approach
  - Dark/light mode support
  - Accessible UI components

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **State Management**: React Context API
- **Styling**: Tailwind CSS with custom components
- **Form Handling**: React Hook Form with Yup validation
- **HTTP Client**: Axios for API requests
- **Icons**: Lucide React
- **Testing**: Jest + React Testing Library

### Backend (API)
- **Framework**: FastAPI (Python 3.10+)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: OpenAPI (Swagger UI)
- **Validation**: Pydantic models
- **CORS**: Enabled for cross-origin requests

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file based on `.env.example`
4. Start the development server:
   ```bash
   npm run dev
   ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
VITE_API_BASE_URL=http://localhost:8000
```

For production, set `VITE_API_BASE_URL` to your production API URL.

## Production Build

To create a production build:

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Deployment

This project is configured for deployment on Netlify with the following settings:

- **Build command:** `npm run build`
- **Publish directory:** `dist`
- **Environment variables:**
  - `VITE_API_BASE_URL`: Your production API URL

## 🌐 API Endpoints

### Profile
- `GET /api/v1/profile` - Get current profile
- `GET /api/v1/profile/all` - List all profiles (paginated)
- `GET /api/v1/profile/{profile_id}` - Get profile by ID
- `POST /api/v1/profile` - Create new profile
- `PUT /api/v1/profile/{profile_id}` - Update profile
- `DELETE /api/v1/profile/{profile_id}` - Delete profile

### Projects
- `GET /api/v1/projects` - List all projects (with filtering)
  - Query Params:
    - `skip`: Number of items to skip (pagination)
    - `limit`: Max items to return (default: 100, max: 100)
    - `featured`: Filter by featured status (true/false)
    - `status`: Filter by project status (active/completed/archived)
    - `skill`: Filter by skill/technology
- `GET /api/v1/projects/{project_id}` - Get project by ID
- `POST /api/v1/projects` - Create new project
- `PUT /api/v1/projects/{project_id}` - Update project
- `DELETE /api/v1/projects/{project_id}` - Delete project

### Search
- `GET /api/v1/search?q={query}` - Search across all content
  - Query Params:
    - `q`: Search query string
    - `limit`: Max results to return (default: 10, max: 50)
    - `type`: Filter by content type (profile/project/all)

### Health Check
- `GET /health` - API health status
- `GET /api/v1/health` - Detailed system health

## 🚀 Live Demo

- **Frontend**:  https://api-jd-w6op-bkab7owk4-ishuraj441s-projects.vercel.app/ "
- **Resume**: [View My Resume](https://docs.google.com/document/d/1rHJgQOykyGm9F88Q9fR3jHr4gkSQvtR4eiUgtZf9F1s/edit?usp=sharing)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) for more information.

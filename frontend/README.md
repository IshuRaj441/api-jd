# Me-API Playground - Frontend

This is the frontend for the Me-API Playground, built with React and Vite. It connects to a FastAPI backend to display profile information, projects, and search functionality.

## Features

- View profile information
- Browse projects filtered by skills
- Search across all content
- Responsive design

## Tech Stack

- React 18
- Vite
- Fetch API for data fetching
- Environment-based configuration

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

## API Endpoints

- `GET /profile` - Get profile information
- `GET /projects?skill={skill}` - Get projects filtered by skill
- `GET /search?q={query}` - Search across all content

## Live Demo

[View Live Demo](https://me-api-playground.netlify.app)

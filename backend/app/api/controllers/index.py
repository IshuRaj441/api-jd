from datetime import datetime

async def get_root():
    return {
        "message": "Welcome to the API JD Backend",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "profile": "/api/profile",
            "projects": "/api/projects",
            "health": "/api/health"
        },
        "documentation": "/docs"
    }

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_projects():
    return [
        {"id": 1, "name": "Project 1"},
        {"id": 2, "name": "Project 2"}
    ]

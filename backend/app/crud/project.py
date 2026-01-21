from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.db.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

def get_project(db: Session, project_id: int) -> Optional[Project]:
    """Get a project by ID."""
    return db.query(Project).filter(Project.id == project_id).first()

def get_projects(
    db: Session, 
    *, 
    skip: int = 0, 
    limit: int = 100,
    featured: Optional[bool] = None,
    status: Optional[str] = None
) -> List[Project]:
    """Get multiple projects with optional filtering and pagination."""
    query = db.query(Project)
    
    if featured is not None:
        query = query.filter(Project.is_featured == featured)
    if status:
        query = query.filter(Project.status == status)
        
    return query.offset(skip).limit(limit).all()

def create_project(db: Session, *, obj_in: ProjectCreate) -> Project:
    """Create a new project."""
    db_obj = Project(
        **obj_in.model_dump(exclude_unset=True),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_project(
    db: Session, *, db_obj: Project, obj_in: ProjectUpdate
) -> Project:
    """Update a project."""
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.model_dump(exclude_unset=True)
    
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_project(db: Session, *, project_id: int) -> Optional[Project]:
    """Delete a project."""
    obj = db.query(Project).get(project_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj

from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Todos
from database import SessionLocal
from .auth import get_current_user

# ⬅ every route in this file gets prefixed with /admin
router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db session
db_dependency = Annotated[Session, Depends(get_db)]

# Access Token Validation
user_dependency = Annotated[dict, Depends(get_current_user)]

"""
ADMIN ENDPOINTS
"""

# Read all todos if user is admin
@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()

# Delete a todo_id if admin

# @router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)

async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed on user or user role')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

    return {"message": "todo deleted"}








from fastapi import FastAPI
import models
from database import engine

""" 
Step 1 of 2: Include auth,py files from routers directory
"""
from routers import auth, todos, admin, users


# Root folder uses our fastAPI Application
app = FastAPI()

# Create a new todoapp db From database/engine
# Only ran if todos.db does not exist
models.Base.metadata.create_all(bind=engine)

    
"""
Step 2 of 2: INCLUDE API Inputs from ROUTERS
"""
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
# FASTAPI entry point
from fastapi import FastAPI
from backend.routes import event
from backend.routes import attendance, users
from backend import models
from backend.database import engine
from fastapi.middleware.cors import CORSMiddleware  # 👈 Add this import
from fastapi.responses import HTMLResponse

app = FastAPI()

# 👇 Add this CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now, later restrict to ["http://localhost:5500"] or wherever frontend runs
    allow_credentials=True,
    allow_methods=["*"],   # allow all methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],   # allow all headers (important for Authorization, Content-Type, etc.)
)

models.Base.metadata.create_all(bind=engine)

app.include_router(event.router, prefix="/events", tags=["Events"])
app.include_router(attendance.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Event Management App is running!"}

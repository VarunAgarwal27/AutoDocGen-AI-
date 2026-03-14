from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from projects import router as projects_router
from dotenv import load_dotenv
load_dotenv()

from database import create_tables
from auth import router as auth_router

app = FastAPI(title="AutoDocGen")


# ALways create a database table after running the program. (ignores if database tables exists.)
@app.on_event("startup")
def startup_event():
    create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication routes

app.include_router(auth_router, prefix="/auth")

app.include_router(projects_router)


# 1st stage of the project (to check the backend is running before fronend conected)
@app.get("/")
def health_check():
    return {"status": "AutoDocGen backend is running 🚀"}

import os
print("GROQ KEY FOUND:", bool(os.getenv("GROQ_API_KEY")))


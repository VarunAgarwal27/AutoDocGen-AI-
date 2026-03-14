from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File, Form
from sqlalchemy.orm import Session
import os
import uuid
import zipfile

from database import SessionLocal
from models import Project, User
from security import decode_access_token

from utils.file_reader import (
    get_project_files,
    read_code_file,
    is_code_file,
    group_files_by_language
)
from utils.file_content_reader import read_project_files
from utils.code_structure_analyzer import analyze_project_files
from utils.prompt_builder import build_prompt
from utils.llm_client import generate_documentation
from utils.doc_exporter import export_pdf, export_docx

from services.github_service import clone_github_repo


router = APIRouter(prefix="/projects", tags=["Projects"])


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Authentication 
def get_current_user(authorization: str, db: Session):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]
    email = decode_access_token(token)

    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Creating project 
@router.post("/create")
def create_project(
    name: str = Form(...),
    repo_url: str = Form(None),
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(authorization, db)

    project = Project(
        name=name,
        repo_url=repo_url,
        user_id=user.id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "message": "Project created successfully 🚀",
        "project_id": project.id
    }


# Access uploaded project
@router.get("/my")
def get_my_projects(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(authorization, db)

    projects = db.query(Project).filter(Project.user_id == user.id).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "repo_url": p.repo_url,
            "zip_path": p.zip_path,
            "extracted_path": p.extracted_path,
            "created_at": p.created_at
        }
        for p in projects
    ]


# Uploading zips files and extraction
@router.post("/upload/{project_id}")
async def upload_project_zip(
    project_id: int,
    file: UploadFile = File(...),
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP files allowed")

    user = get_current_user(authorization, db)

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    os.makedirs("uploads/projects", exist_ok=True)
    os.makedirs("uploads/extracted", exist_ok=True)

    unique_id = str(uuid.uuid4())
    zip_path = f"uploads/projects/{unique_id}.zip"
    extract_path = f"uploads/extracted/{unique_id}"

    contents = await file.read()
    with open(zip_path, "wb") as buffer:
        buffer.write(contents)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    project.zip_path = zip_path
    project.extracted_path = extract_path
    db.commit()

    return {
        "message": "ZIP uploaded & extracted successfully 📦",
        "extracted_path": extract_path
    }


# uploading git hub repo link and cloning the project in temp folder.
@router.post("/github/{project_id}")
def clone_github_project(
    project_id: int,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(authorization, db)

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user.id
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project.repo_url:
        raise HTTPException(status_code=400, detail="GitHub repo URL not set")

    repo_path = clone_github_repo(project.repo_url)

    project.extracted_path = repo_path
    db.commit()

    return {
        "message": "GitHub repository cloned successfully 🚀",
        "extracted_path": repo_path
    }


# uploaded project analysis using Groq AI
@router.get("/{project_id}/analysis")
def analyze_project(
    project_id: int,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(authorization, db)

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user.id
    ).first()

    if not project or not project.extracted_path:
        raise HTTPException(status_code=404, detail="Project not ready")

    grouped = group_files_by_language(project.extracted_path)
    files = read_project_files(grouped)
    analysis = analyze_project_files(files)

    return {
        "project_id": project.id,
        "analysis": analysis
    }


# Generating document file based on analysis.
@router.get("/{project_id}/docs")
def generate_docs(
    project_id: int,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(authorization, db)

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user.id
    ).first()

    if not project or not project.extracted_path:
        raise HTTPException(status_code=404, detail="Project not ready")

    from utils.code_analyzer import analyze_codebase
    from utils.prompt_builder import build_prompt
    from utils.llm_client import generate_documentation

    from utils.semantic_analyzer import semantic_summary

    analysis = analyze_codebase(project.extracted_path)
    if not analysis or not analysis.get("folders"):
        raise HTTPException(status_code=400, detail="Code analysis failed or empty")

    semantic_data = semantic_summary(project.name, analysis)

    prompt = build_prompt(project.name, semantic_data)

    docs = generate_documentation(prompt)

    return {
        "project_id": project.id,
        "documentation": docs
    }




# exporting the docx and pdf file.
@router.get("/{project_id}/export")
def export_docs(
    project_id: int,
    format: str,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(authorization, db)

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user.id
    ).first()

    if not project or not project.extracted_path:
        raise HTTPException(status_code=404, detail="Project not ready")

    from utils.code_analyzer import analyze_codebase
    from utils.prompt_builder import build_prompt
    from utils.llm_client import generate_documentation

    analysis = analyze_codebase(project.extracted_path)

    if not analysis or not analysis.get("folders"):
        raise HTTPException(status_code=400, detail="Code analysis failed or empty")

    prompt = build_prompt(project.name, analysis)
    docs = generate_documentation(prompt)

    os.makedirs("exports", exist_ok=True)

    if format == "pdf":
        path = f"exports/{project.id}.pdf"
        export_pdf(project.name, docs, path)

    elif format == "docx":
        path = f"exports/{project.id}.docx"
        export_docx(project.name, docs, path)

    else:
        raise HTTPException(status_code=400, detail="Invalid format")

    return {
        "message": "Document exported successfully ✅",
        "file_path": path
    }

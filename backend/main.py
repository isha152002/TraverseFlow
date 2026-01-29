# backend/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

from orchestrator import RoadmapOrchestrator
from services import DocumentProcessor
from models.schemas import RoadmapRequest, RoadmapResponse

app = FastAPI(
    title="AI Roadmap Generator",
    description="Multi-agent system for generating intelligent learning roadmaps",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = RoadmapOrchestrator()
doc_processor = DocumentProcessor()

@app.get("/")
async def root():
    return {
        "message": "AI Roadmap Generator API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate_from_text": "/generate-roadmap/text",
            "generate_from_file": "/generate-roadmap/file"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/generate-roadmap/text")
async def generate_roadmap_from_text(request: RoadmapRequest):
    """
    Generate roadmap from text input
    
    Body:
    {
        "text": "Your learning content here..."
    }
    """
    try:
        if not request.text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Generate roadmap
        result = orchestrator.generate_roadmap(request.text)
        
        return RoadmapResponse(
            success=True,
            roadmap=result['roadmap'],
            validation_score=result['validation_score'],
            iterations=result['iterations']
        )
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return RoadmapResponse(
            success=False,
            roadmap=None,
            validation_score=0,
            iterations=0,
            error=str(e)
        )

@app.post("/generate-roadmap/file")
async def generate_roadmap_from_file(file: UploadFile = File(...)):
    """
    Generate roadmap from uploaded file (PDF, DOCX, TXT)
    """
    try:
        # Check file type
        filename = file.filename.lower()
        if filename.endswith('.pdf'):
            file_type = 'pdf'
        elif filename.endswith('.docx'):
            file_type = 'docx'
        elif filename.endswith('.txt'):
            file_type = 'txt'
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload PDF, DOCX, or TXT file."
            )
        
        # Read file content
        file_content = await file.read()
        
        # Extract text
        text = doc_processor.process_file(file_content, file_type)
        
        if not text or len(text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from file"
            )
        
        # Generate roadmap
        result = orchestrator.generate_roadmap(text)
        
        return RoadmapResponse(
            success=True,
            roadmap=result['roadmap'],
            validation_score=result['validation_score'],
            iterations=result['iterations']
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        return RoadmapResponse(
            success=False,
            roadmap=None,
            validation_score=0,
            iterations=0,
            error=str(e)
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
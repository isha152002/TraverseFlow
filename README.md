TraverseFlow
AI-Powered Learning Roadmap Generator

#Overview
TraverseFlow is a multi-agent AI backend system that converts unstructured text or uploaded documents (PDF/DOCX/TXT) into structured learning roadmaps.
The system analyzes educational content and generates:
Organized learning topics
Difficulty levels
Prerequisites and dependencies
Logical learning paths
Recommended learning resources
Project ideas
Validation score for roadmap quality

This project was built to explore LLM-based system design, prompt engineering, and backend AI workflow orchestration.

#Key Features
Accepts raw text or document uploads
Extracts structured topics using LLM APIs
Detects prerequisites and builds dependency relationships
Constructs a logical learning path
Suggests practical resources and project ideas
Includes validation and iterative refinement loop
Provides REST APIs using FastAPI

#Architecture
TraverseFlow follows a modular multi-agent architecture:

Content Analyzer
Extracts topics, difficulty levels, categories, and key concepts.

Prerequisite Detector
Identifies dependencies between topics and determines learning order.

Structure Architect
Builds the roadmap structure including title, overview, and time estimate.

Content Enricher
Adds learning resources and project ideas.

Validator
Scores roadmap quality based on structure and completeness.

Refiner
Iteratively improves the roadmap if validation score is below threshold.

All agents communicate through structured prompt engineering and Groq LLM APIs.

Tech Stack

Programming Language: Python
Backend Framework: FastAPI
LLM Integration: Groq API (LLaMA models)
Document Processing: PyPDF2, python-docx
Other Tools: Pydantic, Uvicorn

API Endpoints

GET /
Returns API information.

GET /health
Health check endpoint.

POST /generate-roadmap/text
Accepts JSON input:
{
"text": "Your learning content here"
}

POST /generate-roadmap/file
Accepts PDF, DOCX, or TXT file upload.

How It Works

User submits text or uploads a document.
Text is extracted and passed to the orchestrator.
Multiple agents sequentially analyze and structure the content.
The roadmap is validated and refined if necessary.
A structured JSON roadmap is returned as output.

Purpose of the Project

TraverseFlow was developed to understand and implement:
Multi-agent LLM orchestration
Prompt-engineered AI workflows
Backend API design using FastAPI
Structured JSON output validation
Iterative refinement systems
It focuses on system design and AI workflow integration rather than model training.

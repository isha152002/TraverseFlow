from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class DifficultyLevel(str, Enum):
    """Represents the difficulty level of a topic/concept in the roadmap"""
    BEGINNER="beginner"
    INTERMEDIATE= "intermediate"
    ADVANCED="advanced"
    EXPERT="expert"

class TopicNode(BaseModel):
    """Represents a single topic/concept in the roadmap"""
    id: str
    topic: str
    description: str
    difficulty_label:DifficultyLevel
    category: str
    time_estimate: str 
    concepts: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    resources: List[Dict[str, str]] = Field(default_factory=list)
    project_ideas: List[str] = Field(default_factory=list)

class RoadmapStructure(BaseModel):
    """Complete roadmap structure"""
    title: str
    overview: str
    total_time_estimate: str
    topics: List[TopicNode]
    dependencies: Dict[str, List[str]] = Field(default_factory=dict)
    learning_path: List[str] = Field(default_factory=list)

class ValidationResult(BaseModel):
    """Result from validation agent"""
    score: int = Field(ge=0, le=100)
    passed: bool
    feedback: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)

class RoadmapRequest(BaseModel):
    """Input schema(text,file) for LLM for roadmap generation"""
    text: Optional[str] = None
    file_content: Optional[str] = None
    file_type: Optional[str] = None

class RoadmapResponse(BaseModel):
    """API response model"""
    success: bool
    roadmap: Optional[RoadmapStructure] = None
    validation_score: int
    iterations: int
    error: Optional[str] = None


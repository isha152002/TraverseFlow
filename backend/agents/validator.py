# backend/agents/validator.py
from .base_agent import BaseAgent
from typing import Dict, Any
import json

class Validator(BaseAgent):
    """Validates roadmap quality and provides feedback"""
    
    def __init__(self, llm_service):
        super().__init__(
            role="Quality Assurance Expert",
            task="Validate roadmap quality and provide improvement feedback",
            llm_service=llm_service
        )
    
    def _build_system_prompt(self) -> str:
        return """You are a quality assurance expert for educational roadmaps.
Your job is to critically evaluate roadmaps and provide actionable feedback.

You check for:
- Logical flow and progression
- Appropriate difficulty scaling
- Complete prerequisite coverage
- Realistic time estimates
- Quality of descriptions and content
- Balance and comprehensiveness

You provide a score from 0-100 and specific feedback for improvement.

Always respond in valid JSON format."""
    
    def _build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        roadmap = input_data.get('roadmap', {})
        
        roadmap_str = json.dumps(roadmap, indent=2)
        
        return f"""Evaluate this learning roadmap and provide a quality score with feedback.

ROADMAP:
{roadmap_str}

Evaluate these aspects:
1. Logical Flow: Does the learning path make sense? (20 points)
2. Prerequisites: Are all prerequisites properly identified? (20 points)
3. Difficulty Progression: Does difficulty increase appropriately? (15 points)
4. Completeness: Are all necessary topics covered? (15 points)
5. Time Estimates: Are time estimates realistic? (10 points)
6. Content Quality: Are descriptions and concepts clear? (10 points)
7. Practical Value: Are project ideas and resources useful? (10 points)

Think step by step:
1. Review each aspect carefully
2. Identify specific issues or missing elements
3. Provide concrete suggestions for improvement
4. Calculate total score

Return ONLY a JSON object with this structure:
{{
  "score": 85,
  "passed": true,
  "feedback": [
    "Issue or observation 1",
    "Issue or observation 2"
  ],
  "suggestions": [
    "Specific suggestion for improvement 1",
    "Specific suggestion for improvement 2"
  ]
}}

Score threshold for passing: 85/100"""
    
   
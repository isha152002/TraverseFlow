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
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            data = json.loads(response)
            # Ensure passed field is set correctly
            data['passed'] = data.get('score', 0) >= 85
            return data
        except json.JSONDecodeError:
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                json_str = response[start:end].strip()
                data = json.loads(json_str)
                data['passed'] = data.get('score', 0) >= 85
                return data
            elif "```" in response:
                start = response.find("```") + 3
                end = response.find("```", start)
                json_str = response[start:end].strip()
                data = json.loads(json_str)
                data['passed'] = data.get('score', 0) >= 85
                return data
            else:
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    data = json.loads(response[start:end])
                    data['passed'] = data.get('score', 0) >= 85
                    return data
                raise ValueError("Could not parse response as JSON")
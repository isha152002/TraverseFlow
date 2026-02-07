# backend/agents/refiner.py
from .base_agent import BaseAgent
from typing import Dict, Any
import json

class Refiner(BaseAgent):
    """Refines roadmap based on validation feedback"""
    
    def __init__(self, llm_service):
        super().__init__(
            role="Roadmap Refinement Specialist",
            task="Improve roadmap based on feedback",
            llm_service=llm_service
        )
    
    def _build_system_prompt(self) -> str:
        return """You are an expert at refining and improving educational roadmaps.
Your job is to take validation feedback and make specific improvements to the roadmap.

You:
- Address all feedback points
- Make concrete improvements
- Maintain the overall structure while enhancing quality
- Fix any logical issues or gaps

Always respond in valid JSON format with the improved roadmap."""
    
    def _build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        roadmap = input_data.get('roadmap', {})
        validation = input_data.get('validation', {})
        
        feedback = validation.get('feedback', [])
        suggestions = validation.get('suggestions', [])
        score = validation.get('score', 0)
        
        feedback_str = "\n".join([f"- {f}" for f in feedback])
        suggestions_str = "\n".join([f"- {s}" for s in suggestions])
        
        roadmap_str = json.dumps(roadmap, indent=2)
        
        return f"""Refine this roadmap based on the validation feedback.

CURRENT ROADMAP:
{roadmap_str}

VALIDATION SCORE: {score}/100

FEEDBACK:
{feedback_str}

SUGGESTIONS FOR IMPROVEMENT:
{suggestions_str}

Make specific improvements to address ALL feedback and suggestions:
1. Fix any logical flow issues
2. Add missing prerequisites
3. Adjust difficulty progression if needed
4. Improve descriptions where needed
5. Enhance time estimates
6. Add or improve resources and projects

Think step by step:
1. Review each piece of feedback
2. Identify what changes are needed
3. Make those changes to the roadmap
4. Ensure all suggestions are addressed

Return ONLY a JSON object with the improved roadmap using the EXACT same structure:
{{
  "title": "...",
  "overview": "...",
  "total_time_estimate": "...",
  "topics": [...]
}}"""
    
    
# backend/agents/content_analyzer.py
from .base_agent import BaseAgent
from typing import Dict, Any
import json

class ContentAnalyzer(BaseAgent):
    """Analyzes content and extracts topics"""
    
    def __init__(self, llm_service):
        super().__init__(
            role="Content Analysis Expert",
            task="Analyze text and extract structured learning topics",
            llm_service=llm_service
        )
    
    def _build_system_prompt(self) -> str:
        return """You are an expert content analyzer specializing in educational material.
Your job is to analyze text and extract all learning topics with detailed metadata.

You must be thorough and identify:
- Main topics and subtopics
- Difficulty levels (1-5 scale)
- Key concepts for each topic
- Appropriate categories

Always respond in valid JSON format."""
    
    def _build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        text = input_data.get('text', '')
        
        return f"""Analyze the following text and extract all learning topics.

TEXT:
{text}

For each topic you identify, provide:
1. topic: Clear, concise topic name
2. description: One sentence description
3. difficulty: Number from 1-5 (1=beginner, 5=expert)
4. difficulty_label: "beginner", "intermediate", "advanced", or "expert"
5. category: Type of content (e.g., "fundamentals", "core concepts", "advanced techniques")
6. concepts: Array of 3-5 key concepts covered in this topic

Think step by step:
1. First, identify all major topics
2. Then, analyze each topic's difficulty
3. Extract key concepts from each
4. Categorize appropriately

Return ONLY a JSON object with this structure:
{{
  "topics": [
    {{
      "topic": "Topic Name",
      "description": "Brief description",
      "difficulty": 3,
      "difficulty_label": "intermediate",
      "category": "core concepts",
      "concepts": ["concept1", "concept2", "concept3"]
    }}
  ]
}}"""
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON response"""
        try:
            # Try direct JSON parse
            data = json.loads(response)
            return data
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                json_str = response[start:end].strip()
                return json.loads(json_str)
            elif "```" in response:
                start = response.find("```") + 3
                end = response.find("```", start)
                json_str = response[start:end].strip()
                return json.loads(json_str)
            else:
                # Try to find JSON object
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    return json.loads(response[start:end])
                raise ValueError("Could not parse response as JSON")
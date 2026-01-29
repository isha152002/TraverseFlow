# backend/agents/prerequisite_detector.py
from .base_agent import BaseAgent
from typing import Dict, Any
import json

class PrerequisiteDetector(BaseAgent):
    """Detects prerequisites and dependencies between topics"""
    
    def __init__(self, llm_service):
        super().__init__(
            role="Learning Path Expert",
            task="Identify prerequisites and learning dependencies",
            llm_service=llm_service
        )
    
    def _build_system_prompt(self) -> str:
        return """You are an expert in learning paths and educational sequencing.
Your job is to analyze topics and determine which concepts must be learned before others.

You understand:
- Foundational concepts that enable understanding of advanced topics
- Logical learning progressions
- Dependencies between concepts

Always respond in valid JSON format."""
    
    def _build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        topics = input_data.get('topics', [])
        
        topics_str = "\n".join([
            f"- {topic['topic']} (Difficulty: {topic['difficulty']}, Category: {topic['category']})"
            for topic in topics
        ])
        
        return f"""Given these topics, identify the prerequisites for each topic.

TOPICS:
{topics_str}

For each topic, determine:
1. What concepts/topics should be learned BEFORE this one
2. Which topics are foundational (no prerequisites)
3. The logical learning order

Think step by step:
1. Identify foundational topics (those with no prerequisites)
2. For each remaining topic, determine what must be learned first
3. Consider difficulty levels - easier topics often come before harder ones
4. Consider logical dependencies in the subject matter

Return ONLY a JSON object with this structure:
{{
  "prerequisites": {{
    "Topic Name": ["prerequisite1", "prerequisite2"],
    "Another Topic": []
  }},
  "learning_path": ["topic1", "topic2", "topic3", ...]
}}

The learning_path should be an ordered list from foundational to advanced topics."""
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            data = json.loads(response)
            return data
        except json.JSONDecodeError:
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
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    return json.loads(response[start:end])
                raise ValueError("Could not parse response as JSON")
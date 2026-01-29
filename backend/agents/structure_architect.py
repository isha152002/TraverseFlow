# backend/agents/structure_architect.py
from .base_agent import BaseAgent
from typing import Dict, Any
import json

class StructureArchitect(BaseAgent):
    """Creates optimal roadmap structure with time estimates"""
    
    def __init__(self, llm_service):
        super().__init__(
            role="Roadmap Structure Expert",
            task="Design optimal learning roadmap structure",
            llm_service=llm_service
        )
    
    def _build_system_prompt(self) -> str:
        return """You are an expert in creating structured learning roadmaps.
Your job is to organize topics into a coherent, well-structured roadmap with realistic time estimates.

You excel at:
- Grouping related topics into modules
- Estimating realistic learning times
- Creating logical progressions
- Balancing depth and breadth

Always respond in valid JSON format."""
    
    def _build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        topics = input_data.get('topics', [])
        prerequisites = input_data.get('prerequisites', {})
        learning_path = input_data.get('learning_path', [])
        
        topics_str = "\n".join([
            f"- {topic['topic']} | Difficulty: {topic['difficulty']} | Concepts: {', '.join(topic['concepts'][:3])}"
            for topic in topics
        ])
        
        return f"""Create a structured roadmap with time estimates for these topics.

TOPICS:
{topics_str}

LEARNING PATH ORDER:
{', '.join(learning_path)}

For each topic, add:
1. time_estimate: Realistic time to learn this topic (e.g., "2-3 hours", "1 week", "2-3 days")
2. Ensure the topic has an id (use format: topic_1, topic_2, etc.)

Also provide:
1. title: A descriptive title for this entire roadmap
2. overview: A 2-3 sentence overview of what this roadmap covers
3. total_time_estimate: Total estimated time for the entire roadmap

Think step by step:
1. Consider the difficulty of each topic
2. Consider the number of concepts in each topic
3. Estimate realistic learning times (be reasonable, not too fast or slow)
4. Sum up total time

Return ONLY a JSON object with this structure:
{{
  "title": "Roadmap Title",
  "overview": "Brief overview of the roadmap",
  "total_time_estimate": "4-6 weeks",
  "topics": [
    {{
      "id": "topic_1",
      "topic": "Topic Name",
      "description": "...",
      "difficulty": 3,
      "difficulty_label": "intermediate",
      "category": "...",
      "time_estimate": "3-4 hours",
      "concepts": ["..."]
    }}
  ]
}}"""
    
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
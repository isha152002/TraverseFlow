# backend/agents/content_enricher.py
from .base_agent import BaseAgent
from typing import Dict, Any
import json

class ContentEnricher(BaseAgent):
    """Enriches topics with resources and project ideas"""
    
    def __init__(self, llm_service):
        super().__init__(
            role="Content Enrichment Specialist",
            task="Add resources and project ideas to topics",
            llm_service=llm_service
        )
    
    def _build_system_prompt(self) -> str:
        return """You are an expert at enriching educational content with practical resources and projects.
Your job is to suggest realistic learning resources and hands-on project ideas.

You provide:
- Specific, practical project ideas
- Realistic resource suggestions (types, not specific URLs unless very well-known)
- Ideas that reinforce learning through practice

Always respond in valid JSON format."""
    
    def _build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        topics = input_data.get('topics', [])
        
        topics_str = "\n\n".join([
            f"Topic: {topic['topic']}\n"
            f"Description: {topic['description']}\n"
            f"Difficulty: {topic['difficulty_label']}\n"
            f"Concepts: {', '.join(topic['concepts'])}"
            for topic in topics
        ])
        
        return f"""For each topic below, suggest resources and project ideas.

TOPICS:
{topics_str}

For each topic, provide:
1. resources: Array of 2-3 learning resources. Each resource should have:
   - type: "documentation", "tutorial", "video", "book", "course", etc.
   - title: Name of the resource
   - description: Brief description (one sentence)

2. project_ideas: Array of 2-3 hands-on project ideas that would help practice this topic
   - Keep projects practical and achievable
   - Projects should directly apply the concepts

Think step by step:
1. Consider what type of resources best suit each topic
2. Think of practical, hands-on projects that reinforce the concepts
3. Keep suggestions realistic and specific

Return ONLY a JSON object with this structure:
{{
  "enriched_topics": [
    {{
      "topic": "Topic Name",
      "resources": [
        {{
          "type": "documentation",
          "title": "Resource Name",
          "description": "Brief description"
        }}
      ],
      "project_ideas": [
        "Project idea 1",
        "Project idea 2"
      ]
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
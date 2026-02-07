# backend/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from services.llm_service import LLMService
import json

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, role: str, task: str, llm_service: LLMService):
        self.role = role
        self.task = task
        self.llm = llm_service
    
    @abstractmethod
    def _build_system_prompt(self) -> str:
        """Build system prompt for this agent"""
        pass
    
    @abstractmethod
    def _build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        """Build user prompt based on input data"""
        pass
    
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
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent
        
        Args:
            input_data: Input dictionary
        
        Returns:
            Structured output dictionary
        """
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(input_data)
        
        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.7
        )
        
        return self._parse_response(response)
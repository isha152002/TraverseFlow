import os
from groq import Groq
from typing import Optional
import json
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    """Service for interacting with GROQ LLM"""
    def __init__(self, model: str="llama-3.1-70b-versatile"):
        """Initialize Groq client"""
        self.api_key=os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in env variables")
        self.client= Groq(api_key=self.api_key)
        self.model = model

    def generate(
        self,
        prompt: str,
        system_prompt : Optional[str]=None,
        temperature: float = 0.7,
        max_tokens: int =4000,
        json_mode: bool =False
    ) -> str:
        """Generates a response from the Groq LLM"""

        messages = []

        if system_prompt: #tells model how to behave
            messages.append({
                "role":"system",
                "content": system_prompt
            })

        messages.append({
            "role":"user",
            "content": prompt
        })

        try:
            completion= self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type":"json_object"} if json_mode else {"type":"text"}
            )

            return completion.choices[0].message.content
        
        except Exception as e:
            print(f"Error calling Groq API:{e}")
            raise
            
    def generate_json(
            self,
            prompt: str,
            system_prompt: Optional[str]=None,
            temperature: float=0.7
    ) -> dict:
        """Generates JSON respone

        Returns:
            Parsed Json dict
        """
        response = self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            json_mode=True
        )

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            #try to extract JSON from response
            start=response.find('{')
            end=response.rfind('}')+1
            if start!=-1 and end!=0 :
                return json.loads(response[start:end])
            raise ValueError("Could not parse JSON response")


# backend/orchestrator.py
from agents import (
    ContentAnalyzer,
    PrerequisiteDetector,
    StructureArchitect,
    ContentEnricher,
    Validator,
    Refiner
)
from services import LLMService
from models.schemas import RoadmapStructure, TopicNode, ValidationResult
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class RoadmapOrchestrator:
    """Orchestrates multi-agent roadmap generation"""
    
    def __init__(self):
        # Initialize LLM service
        self.llm_service = LLMService(model="llama-3.1-70b-versatile")
        
        # Initialize all agents
        self.content_analyzer = ContentAnalyzer(self.llm_service)
        self.prerequisite_detector = PrerequisiteDetector(self.llm_service)
        self.structure_architect = StructureArchitect(self.llm_service)
        self.content_enricher = ContentEnricher(self.llm_service)
        self.validator = Validator(self.llm_service)
        self.refiner = Refiner(self.llm_service)
        
        # Configuration
        self.max_iterations = int(os.getenv("MAX_REFINEMENT_ITERATIONS", "3"))
        self.validation_threshold = int(os.getenv("VALIDATION_THRESHOLD", "85"))
    
    def generate_roadmap(self, text: str) -> Dict[str, Any]:
        """
        Generate roadmap from text using multi-agent system
        
        Args:
            text: Input text to analyze
        
        Returns:
            Dictionary with roadmap and metadata
        """
        print("🚀 Starting roadmap generation...")
        
        # Step 1: Analyze content
        print("\n📊 Step 1: Analyzing content...")
        analysis_result = self.content_analyzer.run({'text': text})
        topics = analysis_result.get('topics', [])
        print(f"   Found {len(topics)} topics")
        
        # Step 2: Detect prerequisites
        print("\n🔍 Step 2: Detecting prerequisites...")
        prereq_result = self.prerequisite_detector.run({'topics': topics})
        prerequisites = prereq_result.get('prerequisites', {})
        learning_path = prereq_result.get('learning_path', [])
        print(f"   Created learning path with {len(learning_path)} steps")
        
        # Step 3: Create structure
        print("\n🏗️  Step 3: Building structure...")
        structure_result = self.structure_architect.run({
            'topics': topics,
            'prerequisites': prerequisites,
            'learning_path': learning_path
        })
        print(f"   Title: {structure_result.get('title', 'N/A')}")
        print(f"   Total time: {structure_result.get('total_time_estimate', 'N/A')}")
        
        # Step 4: Enrich content
        print("\n✨ Step 4: Enriching content...")
        enrichment_result = self.content_enricher.run({
            'topics': structure_result.get('topics', [])
        })
        
        # Merge enrichment into structure
        enriched_topics_map = {
            et['topic']: et for et in enrichment_result.get('enriched_topics', [])
        }
        
        for topic in structure_result.get('topics', []):
            topic_name = topic['topic']
            if topic_name in enriched_topics_map:
                enrichment = enriched_topics_map[topic_name]
                topic['resources'] = enrichment.get('resources', [])
                topic['project_ideas'] = enrichment.get('project_ideas', [])
                topic['prerequisites'] = prerequisites.get(topic_name, [])
        
        # Create initial roadmap
        roadmap = {
            'title': structure_result.get('title', 'Learning Roadmap'),
            'overview': structure_result.get('overview', ''),
            'total_time_estimate': structure_result.get('total_time_estimate', ''),
            'topics': structure_result.get('topics', []),
            'dependencies': prerequisites,
            'learning_path': learning_path
        }
        
        # Step 5: Validation and refinement loop
        print("\n🔄 Step 5: Validation and refinement...")
        iteration = 0
        validation_score = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n   Iteration {iteration}/{self.max_iterations}")
            
            # Validate
            print("   ⚖️  Validating...")
            validation_result = self.validator.run({'roadmap': roadmap})
            validation_score = validation_result.get('score', 0)
            passed = validation_result.get('passed', False)
            
            print(f"   Score: {validation_score}/100")
            
            if passed:
                print("   ✅ Validation passed!")
                break
            
            if iteration >= self.max_iterations:
                print("   ⚠️  Max iterations reached")
                break
            
            # Refine
            print("   🔧 Refining roadmap...")
            refined = self.refiner.run({
                'roadmap': roadmap,
                'validation': validation_result
            })
            
            # Update roadmap
            roadmap.update(refined)
        
        print(f"\n✅ Roadmap generation complete!")
        print(f"   Final score: {validation_score}/100")
        print(f"   Iterations: {iteration}")
        
        return {
            'roadmap': roadmap,
            'validation_score': validation_score,
            'iterations': iteration
        }
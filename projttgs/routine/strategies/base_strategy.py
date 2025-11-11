"""
Abstract base strategy for routine generation.
Following Strategy Pattern and Open/Closed Principle.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseGenerationStrategy(ABC):
    """
    Abstract base class for routine generation strategies.
    Following Open/Closed Principle - can be extended without modification.
    """
    
    @abstractmethod
    def generate(self, **kwargs) -> Dict[str, Any]:
        """
        Generate a routine/timetable.
        
        Args:
            **kwargs: Strategy-specific parameters
            
        Returns:
            Dictionary containing generated routine data
        """
        pass
    
    @abstractmethod
    def get_fitness(self, schedule: Any) -> float:
        """
        Calculate fitness score for a schedule.
        
        Args:
            schedule: Schedule object to evaluate
            
        Returns:
            Fitness score (higher is better)
        """
        pass


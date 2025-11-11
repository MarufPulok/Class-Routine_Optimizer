"""
Factory for creating routine generation strategies.
Following Factory Pattern - centralizes strategy creation.
"""
from typing import Optional
from routine.strategies.base_strategy import BaseGenerationStrategy
from routine.strategies.genetic_algorithm_strategy import GeneticAlgorithmStrategy
from core.exceptions import ValidationError


class GenerationFactory:
    """
    Factory for creating generation strategies.
    Following Factory Pattern and Open/Closed Principle.
    """
    
    @staticmethod
    def create_strategy(strategy_type: str = 'genetic_algorithm', **kwargs) -> BaseGenerationStrategy:
        """
        Create a generation strategy based on type.
        
        Args:
            strategy_type: Type of strategy ('genetic_algorithm', etc.)
            **kwargs: Strategy-specific parameters
            
        Returns:
            Strategy instance
            
        Raises:
            ValidationError: If strategy type is invalid
        """
        if strategy_type == 'genetic_algorithm':
            return GeneticAlgorithmStrategy(**kwargs)
        else:
            raise ValidationError(f"Unknown strategy type: {strategy_type}")
    
    @staticmethod
    def get_default_strategy() -> BaseGenerationStrategy:
        """Get the default generation strategy."""
        return GenerationFactory.create_strategy('genetic_algorithm')


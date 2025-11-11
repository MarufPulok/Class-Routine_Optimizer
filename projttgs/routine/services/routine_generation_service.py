"""
Routine generation service.
Following Single Responsibility Principle - handles routine generation business logic only.
"""
from typing import Dict, Any
from routine.factories.generation_factory import GenerationFactory
from routine.strategies.base_strategy import BaseGenerationStrategy
from core.services.base import BaseService
from core.exceptions import RoutineGenerationError


class RoutineGenerationService(BaseService):
    """
    Service for routine generation operations.
    Following Dependency Inversion Principle - depends on strategy abstraction.
    """
    
    def __init__(self, strategy: BaseGenerationStrategy = None):
        """
        Initialize service with a generation strategy.
        
        Args:
            strategy: Generation strategy (defaults to genetic algorithm)
        """
        super().__init__()
        self.strategy = strategy or GenerationFactory.get_default_strategy()
    
    def generate_routine(self, strategy_type: str = 'genetic_algorithm', **kwargs) -> Dict[str, Any]:
        """
        Generate a routine/timetable.
        
        Args:
            strategy_type: Type of generation strategy to use
            **kwargs: Strategy-specific parameters
            
        Returns:
            Dictionary with generated routine data
            
        Raises:
            RoutineGenerationError: If generation fails
        """
        try:
            # Create strategy if different from current
            if strategy_type != 'genetic_algorithm' or self.strategy is None:
                self.strategy = GenerationFactory.create_strategy(strategy_type, **kwargs)
            
            result = self.strategy.generate(**kwargs)
            
            self.log_info(
                f"Routine generated successfully: "
                f"fitness={result.get('fitness', 0)}, "
                f"generations={result.get('generations', 0)}"
            )
            
            return result
        except Exception as e:
            self.log_error("Error generating routine", error=e)
            raise RoutineGenerationError(f"Failed to generate routine: {str(e)}")


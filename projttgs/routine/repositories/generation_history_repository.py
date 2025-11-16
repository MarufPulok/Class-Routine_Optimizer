"""
Generation history repository implementation.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from core.repositories.mongodb_repository import MongoDBRepository
from routine.models import GenerationHistory


class GenerationHistoryRepository(MongoDBRepository[GenerationHistory]):
    """Repository for GenerationHistory model."""
    
    def __init__(self):
        super().__init__(GenerationHistory)
    
    def get_latest(self, limit: int = 10) -> List[GenerationHistory]:
        """
        Get latest generation history records.
        
        Args:
            limit: Number of records to return
            
        Returns:
            List of latest generation history records
        """
        return list(self.model.objects.order_by('-timestamp')[:limit])
    
    def get_by_date_range(
        self,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> List[GenerationHistory]:
        """
        Get generation history within a date range.
        
        Args:
            date_from: Start date (inclusive)
            date_to: End date (inclusive)
            
        Returns:
            List of generation history records in date range
        """
        queryset = self.model.objects
        
        if date_from:
            queryset = queryset.filter(timestamp__gte=date_from)
        if date_to:
            queryset = queryset.filter(timestamp__lte=date_to)
        
        return list(queryset.order_by('-timestamp'))
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get aggregate statistics from generation history.
        
        Returns:
            Dictionary with statistics: total_generations, average_fitness, best_fitness
        """
        all_history = list(self.model.objects.all())
        
        if not all_history:
            return {
                'total_generations': 0,
                'average_fitness': 0.0,
                'best_fitness': 0.0,
                'total_conflicts': 0,
                'average_conflicts': 0.0,
                'success_count': 0,
                'failed_count': 0
            }
        
        successful = [h for h in all_history if h.status == 'Success']
        fitness_scores = [h.fitness_score for h in successful if h.fitness_score is not None]
        conflict_counts = [h.conflicts_count for h in successful if h.conflicts_count is not None]
        
        return {
            'total_generations': len(all_history),
            'average_fitness': sum(fitness_scores) / len(fitness_scores) if fitness_scores else 0.0,
            'best_fitness': max(fitness_scores) if fitness_scores else 0.0,
            'total_conflicts': sum(conflict_counts) if conflict_counts else 0,
            'average_conflicts': sum(conflict_counts) / len(conflict_counts) if conflict_counts else 0.0,
            'success_count': len(successful),
            'failed_count': len(all_history) - len(successful)
        }


"""
Generation strategies for routine generation.
Following Strategy Pattern - allows swapping algorithms.
"""
from .base_strategy import BaseGenerationStrategy
from .genetic_algorithm_strategy import GeneticAlgorithmStrategy

__all__ = ['BaseGenerationStrategy', 'GeneticAlgorithmStrategy']


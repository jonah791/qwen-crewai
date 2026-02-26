"""
Main CrewAI module initialization
"""

# Import classes with delayed evaluation to avoid circular imports
from .agent import Agent
from .task import Task
from .crew import Crew

__all__ = ['Agent', 'Task', 'Crew']
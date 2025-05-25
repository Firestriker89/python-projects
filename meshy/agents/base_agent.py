"""
Base Agent Module

This module contains the abstract base class for all agents in the system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the meshy system.
    
    Defines the common interface and functionality that all agents must implement.
    """
    
    def __init__(self, agent_id: str, name: str, config: Optional[Dict[str, Any]] = None):
        self.agent_id = agent_id
        self.name = name
        self.config = config or {}
        self.created_at = datetime.now()
        self.is_active = True
        
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        Process input data and return output.
        
        Args:
            input_data: The data to process
            
        Returns:
            Processed output data
        """
        pass
        
    @abstractmethod
    def update_state(self, new_state: Dict[str, Any]) -> None:
        """
        Update the agent's internal state.
        
        Args:
            new_state: Dictionary containing new state information
        """
        pass
        
    def activate(self) -> None:
        """Activate the agent."""
        self.is_active = True
        
    def deactivate(self) -> None:
        """Deactivate the agent."""
        self.is_active = False
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.agent_id}, name={self.name})"

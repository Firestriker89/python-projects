"""
Human Agent Module

This module contains the HumanAgent class for representing human participants.
"""

from typing import Any, Dict, Optional
from .base_agent import BaseAgent


class HumanAgent(BaseAgent):
    """
    Represents a human agent in the system.
    
    Human agents can interact with the system through various interfaces
    and provide human input and decision-making capabilities.
    """
    
    def __init__(self, 
                 agent_id: str, 
                 name: str, 
                 config: Optional[Dict[str, Any]] = None,
                 interface_type: str = "console"):
        super().__init__(agent_id, name, config)
        self.interface_type = interface_type
        self.interaction_history = []
        
    def process(self, input_data: Any) -> Any:
        """
        Process input by presenting it to the human and collecting response.
        
        Args:
            input_data: The data to present to the human
            
        Returns:
            Human's response/decision
        """
        if not self.is_active:
            return None
            
        # Record the interaction
        interaction = {
            "timestamp": self.created_at,
            "input": input_data,
            "response": None
        }
        
        if self.interface_type == "console":
            response = self._console_interaction(input_data)
        else:
            response = self._default_interaction(input_data)
            
        interaction["response"] = response
        self.interaction_history.append(interaction)
        
        return response
        
    def update_state(self, new_state: Dict[str, Any]) -> None:
        """
        Update the human agent's state and preferences.
        
        Args:
            new_state: Dictionary containing new state information
        """
        if "preferences" in new_state:
            self.config.update(new_state["preferences"])
            
        if "interface_type" in new_state:
            self.interface_type = new_state["interface_type"]
            
    def _console_interaction(self, input_data: Any) -> str:
        """Handle console-based interaction with human."""
        print(f"\n[{self.name}] Input: {input_data}")
        response = input(f"[{self.name}] Your response: ")
        return response
        
    def _default_interaction(self, input_data: Any) -> Any:
        """Default interaction method."""
        # For now, return a placeholder response
        return f"Human response to: {input_data}"
        
    def get_interaction_count(self) -> int:
        """Get the total number of interactions."""
        return len(self.interaction_history)

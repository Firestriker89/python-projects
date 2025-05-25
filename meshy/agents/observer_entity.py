"""
Observer Entity Module

This module contains the ObserverEntity class for monitoring and observing system states.
"""

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from .base_agent import BaseAgent


class ObserverEntity(BaseAgent):
    """
    Observer entity that monitors and records system states and events.
    
    Observers can watch specific events, states, or agent behaviors and
    trigger actions based on observed patterns.
    """
    
    def __init__(self, 
                 agent_id: str, 
                 name: str, 
                 config: Optional[Dict[str, Any]] = None,
                 observation_targets: Optional[List[str]] = None):
        super().__init__(agent_id, name, config)
        self.observation_targets = observation_targets or []
        self.observations = []
        self.triggers = {}
        self.is_monitoring = False
        
    def process(self, input_data: Any) -> Any:
        """
        Process input by observing and recording it.
        
        Args:
            input_data: The data to observe
            
        Returns:
            Observation record
        """
        if not self.is_active or not self.is_monitoring:
            return None
            
        observation = self._create_observation(input_data)
        self.observations.append(observation)
        
        # Check for triggers
        self._check_triggers(observation)
        
        return observation
        
    def update_state(self, new_state: Dict[str, Any]) -> None:
        """
        Update the observer's state and configuration.
        
        Args:
            new_state: Dictionary containing new state information
        """
        if "observation_targets" in new_state:
            self.observation_targets = new_state["observation_targets"]
            
        if "monitoring" in new_state:
            self.is_monitoring = new_state["monitoring"]
            
    def start_monitoring(self) -> None:
        """Start monitoring observations."""
        self.is_monitoring = True
        
    def stop_monitoring(self) -> None:
        """Stop monitoring observations."""
        self.is_monitoring = False
        
    def add_trigger(self, trigger_name: str, condition: Callable, action: Callable) -> None:
        """
        Add a trigger that executes an action when a condition is met.
        
        Args:
            trigger_name: Name of the trigger
            condition: Function that takes an observation and returns bool
            action: Function to execute when condition is true
        """
        self.triggers[trigger_name] = {
            "condition": condition,
            "action": action,
            "triggered_count": 0
        }
        
    def remove_trigger(self, trigger_name: str) -> None:
        """Remove a trigger by name."""
        if trigger_name in self.triggers:
            del self.triggers[trigger_name]
            
    def get_observations(self, 
                        target: Optional[str] = None, 
                        since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Get observations, optionally filtered by target and time.
        
        Args:
            target: Filter by observation target
            since: Filter by observations since this datetime
            
        Returns:
            List of matching observations
        """
        filtered_observations = self.observations
        
        if target:
            filtered_observations = [
                obs for obs in filtered_observations 
                if obs.get("target") == target
            ]
            
        if since:
            filtered_observations = [
                obs for obs in filtered_observations 
                if obs.get("timestamp", datetime.min) >= since
            ]
            
        return filtered_observations
        
    def _create_observation(self, input_data: Any) -> Dict[str, Any]:
        """Create an observation record."""
        return {
            "timestamp": datetime.now(),
            "observer_id": self.agent_id,
            "data": input_data,
            "target": getattr(input_data, "target", None),
            "type": type(input_data).__name__
        }
        
    def _check_triggers(self, observation: Dict[str, Any]) -> None:
        """Check if any triggers should be activated."""
        for trigger_name, trigger_config in self.triggers.items():
            try:
                if trigger_config["condition"](observation):
                    trigger_config["action"](observation)
                    trigger_config["triggered_count"] += 1
            except Exception as e:
                print(f"Error in trigger {trigger_name}: {e}")
                
    def get_statistics(self) -> Dict[str, Any]:
        """Get observer statistics."""
        return {
            "total_observations": len(self.observations),
            "is_monitoring": self.is_monitoring,
            "active_triggers": len(self.triggers),
            "observation_targets": self.observation_targets
        }

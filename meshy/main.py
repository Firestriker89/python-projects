"""
Meshy - Main Application Entry Point

This is the main entry point for the Meshy system, which provides a framework
for managing timelines, agents, and reality conflicts.
"""

import sys
from datetime import datetime
from typing import Dict, Any

from config import Config
from timeline.node import Node
from agents.base_agent import BaseAgent
from agents.human_agent import HumanAgent
from agents.observer_entity import ObserverEntity
from reality.conflict_resolver import ConflictResolver, ConflictType


class MeshySystem:
    """
    Main system class that orchestrates all components of the Meshy framework.
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.timeline_root = Node("root", datetime.now(), {"type": "system_start"})
        self.agents = {}
        self.observers = {}
        self.conflict_resolver = ConflictResolver()
        self.system_state = {"initialized": True, "running": False}
        
    def add_agent(self, agent: BaseAgent) -> None:
        """Add an agent to the system."""
        self.agents[agent.agent_id] = agent
        print(f"Added agent: {agent.name} ({agent.agent_id})")
        
    def add_observer(self, observer: ObserverEntity) -> None:
        """Add an observer to the system."""
        self.observers[observer.agent_id] = observer
        print(f"Added observer: {observer.name} ({observer.agent_id})")
        
    def start_system(self) -> None:
        """Start the Meshy system."""
        print("Starting Meshy system...")
        self.system_state["running"] = True
        
        # Start all observers
        for observer in self.observers.values():
            observer.start_monitoring()
            
        print("Meshy system started successfully!")
        
    def stop_system(self) -> None:
        """Stop the Meshy system."""
        print("Stopping Meshy system...")
        self.system_state["running"] = False
        
        # Stop all observers
        for observer in self.observers.values():
            observer.stop_monitoring()
            
        print("Meshy system stopped.")
        
    def process_input(self, agent_id: str, input_data: Any) -> Any:
        """Process input through a specific agent."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
            
        agent = self.agents[agent_id]
        result = agent.process(input_data)
        
        # Notify observers
        for observer in self.observers.values():
            observer.process({
                "agent_id": agent_id,
                "input": input_data,
                "output": result,
                "timestamp": datetime.now()
            })
            
        return result
        
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return {
            "running": self.system_state["running"],
            "agents": len(self.agents),
            "observers": len(self.observers),
            "conflicts_resolved": len(self.conflict_resolver.conflict_history),
            "timeline_nodes": len(self.timeline_root.children) + 1
        }


def create_demo_system() -> MeshySystem:
    """Create a demo system with sample agents and observers."""
    config = Config()
    system = MeshySystem(config)
    
    # Add a human agent
    human_agent = HumanAgent("human_1", "Demo Human", {"interface_type": "console"})
    system.add_agent(human_agent)
    
    # Add an observer
    observer = ObserverEntity("observer_1", "System Observer", 
                             observation_targets=["human_1"])
    system.add_observer(observer)
    
    return system


def main():
    """Main function to run the Meshy system."""
    print("Welcome to Meshy!")
    print("=" * 50)
    
    try:
        # Create and start the system
        system = create_demo_system()
        system.start_system()
        
        # Show system status
        status = system.get_system_status()
        print(f"\nSystem Status: {status}")
        
        # Demo interaction
        print("\nDemo: Processing input through human agent...")
        result = system.process_input("human_1", "Hello, Meshy system!")
        print(f"Result: {result}")
        
        # Show final status
        final_status = system.get_system_status()
        print(f"\nFinal Status: {final_status}")
        
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'system' in locals():
            system.stop_system()
        print("Goodbye!")


if __name__ == "__main__":
    main()

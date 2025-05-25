"""
Timeline Node Module

This module contains the Node class for representing timeline events and states.
"""

from typing import Any, Dict, Optional, List
from datetime import datetime


class Node:
    """
    Represents a node in the timeline system.
    
    Each node can represent an event, state, or decision point in the timeline.
    """
    
    def __init__(self, 
                 node_id: str, 
                 timestamp: Optional[datetime] = None,
                 data: Optional[Dict[str, Any]] = None,
                 parent: Optional['Node'] = None):
        self.node_id = node_id
        self.timestamp = timestamp or datetime.now()
        self.data = data or {}
        self.parent = parent
        self.children: List['Node'] = []
        
    def add_child(self, child: 'Node') -> None:
        """Add a child node to this node."""
        child.parent = self
        self.children.append(child)
        
    def get_path(self) -> List['Node']:
        """Get the path from root to this node."""
        path = []
        current = self
        while current:
            path.insert(0, current)
            current = current.parent
        return path
        
    def __repr__(self) -> str:
        return f"Node(id={self.node_id}, timestamp={self.timestamp})"

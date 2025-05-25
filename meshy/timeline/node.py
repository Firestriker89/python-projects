from typing import List, Optional, Dict, Any
from datetime import datetime

class TimelineNode:
    """
    A commit-like representation of an event in the timeline.
    Stores when and where it occurred, what was perceived,
    the agent's state, and its relation to other timeline branches.
    """

    def __init__(
        self,
        t: datetime,
        position: tuple[float, float, float],
        event_data: Dict[str, Any],
        intent_meta: Optional[Dict[str, Any]] = None,
        branch_id: Optional[str] = None,
        agent_id: Optional[str] = None
    ):
        self.t = t  # Absolute timestamp
        self.position = position  # x, y, z in space
        self.event_data = event_data  # Sensory + contextual payload
        self.intent_meta = intent_meta or {}  # Motivation, emotion, awareness
        self.branch_id = branch_id or "main"  # Timeline identity
        self.agent_id = agent_id  # Originating agent
        
        self.parents: List["TimelineNode"] = []
        self.children: List["TimelineNode"] = []

    def add_child(self, child_node: "TimelineNode"):
        self.children.append(child_node)
        child_node.parents.append(self)

    def summary(self) -> str:
        return f"[{self.t.isoformat()}] @ {self.position} by {self.agent_id or 'unknown'}"

    def __repr__(self):
        return f"<TimelineNode {self.summary()} branch={self.branch_id}>"

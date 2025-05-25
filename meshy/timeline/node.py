from datetime import datetime
from typing import List, Optional, Dict, Any

class TimelineNode:
    """
    Represents a snapshot of perceived reality as experienced by an agent at a point in time and space.
    Includes event content, intent metadata (emotion, certainty, etc.), and branching structure.
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
        self.t = t  # absolute timestamp
        self.position = position  # (x, y, z) in conceptual or simulated space
        self.event_data = event_data  # what was observed
        self.intent_meta = intent_meta or {
            "emotion": "neutral",     # default affect
            "certainty": 0.5,         # 0 to 1.0 scale
            "bias": None,             # optional semantic tag
            "focus": 1.0              # how much attention was given
        }
        self.branch_id = branch_id or "main"
        self.agent_id = agent_id

        # Relationships to other timeline nodes
        self.parents: List["TimelineNode"] = []
        self.children: List["TimelineNode"] = []

    def add_child(self, child_node: "TimelineNode"):
        """Link this node to a child node."""
        self.children.append(child_node)
        child_node.parents.append(self)

    def summary(self) -> str:
        return f"[{self.t.isoformat()}] @ {self.position} by {self.agent_id or 'unknown'}"

    def __repr__(self):
        return f"<TimelineNode {self.summary()} branch={self.branch_id}>"

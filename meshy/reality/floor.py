from typing import List
from timeline.node import TimelineNode
from datetime import datetime

class FloorTag:
    """
    Represents a snapshot or release version of a timeline.
    Used by observer entities to tag key frames of canonical reality.
    """

    def __init__(self, tag_name: str, nodes: List[TimelineNode], created_at: datetime):
        self.tag_name = tag_name
        self.nodes = nodes  # All nodes included in this tagged floor
        self.created_at = created_at

    def summary(self) -> str:
        return f"FloorTag[{self.tag_name}] - {len(self.nodes)} nodes @ {self.created_at.isoformat()}"

    def get_agents(self) -> List[str]:
        return list({node.agent_id for node in self.nodes if node.agent_id})

    def get_branches(self) -> List[str]:
        return list({node.branch_id for node in self.nodes})

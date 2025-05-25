from datetime import datetime
from typing import List, Dict, Any
from timeline.node import TimelineNode

class HumanAgent:
    """
    Represents a human observer.
    Capable of perceiving events and committing them as TimelineNodes.
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.memory: List[TimelineNode] = []

    def perceive_event(
        self,
        t: datetime,
        position: tuple[float, float, float],
        event_data: Dict[str, Any],
        intent_meta: Dict[str, Any] = {}
    ) -> TimelineNode:
        """
        Simulates the perception of an event at a point in time and space.
        Commits it to the agent's memory as a TimelineNode.
        """
        node = TimelineNode(
            t=t,
            position=position,
            event_data=event_data,
            intent_meta=intent_meta,
            branch_id="main",
            agent_id=self.agent_id
        )
        self.memory.append(node)
        return node

    def get_memory_summary(self) -> List[str]:
        return [node.summary() for node in self.memory]

    def __repr__(self):
        return f"<HumanAgent {self.agent_id} | {len(self.memory)} memorie_s>"
from typing import List, Tuple, Dict
from agents.human_agent import HumanAgent
from timeline.node import TimelineNode

class ObserverEntity:
    """
    Represents a higher-dimensional observer.
    Can compare timelines from multiple agents and detect conflicts.
    """

    def __init__(self, observer_id: str = "observer_0"):
        self.observer_id = observer_id

    def detect_conflicts(self, agents: List[HumanAgent]) -> List[Tuple[TimelineNode, TimelineNode]]:
        """
        Compares timeline nodes from different agents to detect contradictory memories.
        Returns a list of node pairs that conflict in event data but overlap in time and position.
        """
        conflicts = []
        all_nodes = [(agent.agent_id, node) for agent in agents for node in agent.memory]

        for i in range(len(all_nodes)):
            id1, node1 = all_nodes[i]
            for j in range(i + 1, len(all_nodes)):
                id2, node2 = all_nodes[j]

                if id1 != id2 and self._is_conflicting(node1, node2):
                    conflicts.append((node1, node2))

        return conflicts

    def _is_conflicting(self, node1: TimelineNode, node2: TimelineNode) -> bool:
        """
        Basic conflict check: same time and position but different observed event.
        This is placeholder logic and will evolve.
        """
        same_time = node1.t == node2.t
        same_place = node1.position == node2.position
        different_event = node1.event_data != node2.event_data

        return same_time and same_place and different_event

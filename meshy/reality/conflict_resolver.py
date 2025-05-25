from typing import List, Tuple
from timeline.node import TimelineNode

class ConflictResolver:
    """
    Resolves conflicting timeline nodes according to specified strategy.
    Can merge, reject, or create divergent branches.
    """

    def __init__(self, strategy: str = "merge"):
        """
        Strategy options:
        - 'merge': blend both events into a reconciled node
        - 'reject': remove both conflicting nodes
        - 'split': create divergent timeline branches
        """
        self.strategy = strategy

    def resolve(self, conflicts: List[Tuple[TimelineNode, TimelineNode]]) -> List[TimelineNode]:
        resolved_nodes = []

        for node_a, node_b in conflicts:
            if self.strategy == "merge":
                merged = self._merge_nodes(node_a, node_b)
                resolved_nodes.append(merged)

            elif self.strategy == "reject":
                # Ignore both conflicting nodes
                continue

            elif self.strategy == "split":
                # Mark nodes as diverging into new branches
                node_a.branch_id = f"{node_a.branch_id}_a"
                node_b.branch_id = f"{node_b.branch_id}_b"
                resolved_nodes.extend([node_a, node_b])

        return resolved_nodes

    def _merge_nodes(self, node_a: TimelineNode, node_b: TimelineNode) -> TimelineNode:
        """
        Merges two conflicting nodes into a new node by combining metadata.
        Assumes time and position are the same.
        """
        merged_event = {
            "description": f"[MERGED] {node_a.event_data['description']} / {node_b.event_data['description']}"
        }

        merged_intent = {
            **node_a.intent_meta,
            **node_b.intent_meta,
            "merged_from": [node_a.agent_id, node_b.agent_id]
        }

        return TimelineNode(
            t=node_a.t,
            position=node_a.position,
            event_data=merged_event,
            intent_meta=merged_intent,
            branch_id="merged",
            agent_id="system"
        )

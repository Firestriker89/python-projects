from datetime import datetime
from typing import List, Dict, Any
from agents.observer_entity import ObserverEntity
from reality.conflict_resolver import ConflictResolver
from reality.floor import FloorTag
from timeline.node import TimelineNode

class ObserverScriptEngine:
    """
    Allows an observer to execute commands to manipulate the timeline structure.
    """

    def __init__(self, observer: ObserverEntity):
        self.observer = observer
        self.log: List[str] = []
        self.floor_tags: List[FloorTag] = []

    def execute(self, command: str, context: Dict[str, Any]) -> Any:
        """
        Parses and executes a structured observer command.
        `context` should include access to agent memories, conflicts, or nodes.
        """
        self.log.append(command)
        cmd = command.strip().lower()

        if cmd.startswith("merge"):
            resolver = ConflictResolver(strategy="merge")
            return resolver.resolve(context.get("conflicts", []))

        elif cmd.startswith("split"):
            resolver = ConflictResolver(strategy="split")
            return resolver.resolve(context.get("conflicts", []))

        elif cmd.startswith("reject"):
            resolver = ConflictResolver(strategy="reject")
            return resolver.resolve(context.get("conflicts", []))

        elif cmd.startswith("tag floor"):
            tag_name = command.split(" ")[-1]
            nodes = context.get("nodes", [])
            tag = FloorTag(tag_name, nodes, created_at=datetime.utcnow())
            self.floor_tags.append(tag)
            return tag

        elif cmd.startswith("log"):
            return self.log

        elif cmd.startswith("mask certainty <"):
            try:
                threshold = float(cmd.split("<")[-1].strip())
                original = context.get("nodes", [])
                filtered = [node for node in original if node.intent_meta.get("certainty", 0.5) >= threshold]
                context["nodes"] = filtered
                return f"Masked nodes with certainty < {threshold}. {len(filtered)} remaining."
            except Exception as e:
                return f"Invalid certainty threshold: {e}"
        else:
            raise ValueError(f"Unknown observer command: {command}")


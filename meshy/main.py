from datetime import datetime
from agents.human_agent import HumanAgent
from agents.observer_entity import ObserverEntity
from reality.conflict_resolver import ConflictResolver
from config import DEFAULT_RESOLUTION_STRATEGY
resolver = ConflictResolver(strategy=DEFAULT_RESOLUTION_STRATEGY)
from visualization.render_3d import render_timeline_nodes

# Step 1: Create two human agents
agent_a = HumanAgent("agent_alpha")
agent_b = HumanAgent("agent_beta")

# Step 2: Both perceive events at the same time and place, but disagree
agent_a.perceive_event(
    t=datetime(1983, 7, 12, 12, 0),
    position=(0, 0, 0),
    event_data={"description": "Mandela funeral"},
    intent_meta={"emotion": "grief"}
)

agent_b.perceive_event(
    t=datetime(1983, 7, 12, 12, 0),
    position=(0, 0, 0),
    event_data={"description": "Mandela speech at UN"},
    intent_meta={"emotion": "hope"}
)

# Step 3: Observer detects timeline divergence
observer = ObserverEntity()
conflicts = observer.detect_conflicts([agent_a, agent_b])

print(f"\nObserver detected {len(conflicts)} conflict(s):")
for c1, c2 in conflicts:
    print(f"→ Conflict between:\n  A: {c1.summary()}\n  B: {c2.summary()}")

# Step 4: Resolve conflict using strategy (merge, reject, split)
resolver = ConflictResolver(strategy="merge")
resolved = resolver.resolve(conflicts)

print(f"\nResolved {len(resolved)} node(s):")
for r in resolved:
    print(r)

if resolved:
    render_timeline_nodes(resolved, title="Resolved Timeline")

from reality.floor import FloorTag
from datetime import datetime

# Create tag from resolved nodes
floor = FloorTag(tag_name="floor_1983.v1", nodes=resolved, created_at=datetime.utcnow())

print(floor.summary())
print("Agents in tag:", floor.get_agents())
print("Branches in tag:", floor.get_branches())
from visualization.branch_graph import render_branch_graph

# Graph includes all agent memories and any resolved/merged nodes
render_branch_graph(agent_a.memory + agent_b.memory + resolved, title="Meshy Timeline Branch Graph")
from agents.observer_script import ObserverScriptEngine

engine = ObserverScriptEngine(observer)

# Merge timeline as observer
resolved = engine.execute("merge conflicts", context={"conflicts": conflicts})

# Tag result
floor = engine.execute("tag floor floor_1983.v2", context={"nodes": resolved})

# Print log of observer's actions
print("\nObserver Actions:")
for entry in engine.log:
    print(" -", entry)

print(f"\nCreated floor tag: {floor.summary()}")
from visualization.branch_graph import render_branch_graph
from visualization.observer_view import render_observer_view

context = {"conflicts": conflicts, "nodes": resolved}

while True:
    cmd = input("\n[observer]> ").strip()
    if cmd.lower() in {"exit", "quit"}:
        break
    try:
        result = engine.execute(cmd, context=context)

        # Update visualization after every command
        merged_nodes = context.get("nodes", [])  # This should be updated if 'merge' returns something
        render_observer_view(agent_a.memory + agent_b.memory + merged_nodes, title="Observer View")
        render_branch_graph(agent_a.memory + agent_b.memory + merged_nodes, title="Branch Graph")

        print("→", result if not isinstance(result, list) else f"{len(result)} item(s) affected.")
        
        # Optionally: update context
        if cmd.startswith("merge"):
            context["nodes"] = result

    except Exception as e:
        print("Error:", e)

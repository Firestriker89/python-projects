import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.human_agent import HumanAgent
from agents.observer_entity import ObserverEntity
from agents.observer_script import ObserverScriptEngine
from reality.conflict_resolver import ConflictResolver
from datetime import datetime
from visualization.observer_view import render_timeline_nodes
from visualization.branch_graph import render_branch_graph
import plotly.graph_objects as go

# --- Setup dummy agents and events (real code would load from memory or file) ---
agent_a = HumanAgent("agent_alpha")
agent_b = HumanAgent("agent_beta")

# Create conflicting memories
agent_a.perceive_event(
    t=datetime(1983, 7, 12, 12, 0),
    position=(0, 0, 0),
    event_data={"description": "Mandela funeral"},
)

agent_b.perceive_event(
    t=datetime(1983, 7, 12, 12, 0),
    position=(0, 0, 0),
    event_data={"description": "Mandela speech at UN"},
)

# Detect conflicts and prepare engine
observer = ObserverEntity()
conflicts = observer.detect_conflicts([agent_a, agent_b])
engine = ObserverScriptEngine(observer)

context = {
    "conflicts": conflicts,
    "nodes": []
}

# --- Dash App ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Meshy Observer Mode"

def get_3d_fig():
    return render_timeline_nodes(agent_a.memory + agent_b.memory + context.get("nodes", []), title="Observer View", return_fig=True)

def get_branch_fig():
    return render_branch_graph(agent_a.memory + agent_b.memory + context.get("nodes", []), title="Branch Graph", return_fig=True)

app.layout = dbc.Container([
    html.H1("Meshy – Observer Mode", className="my-3"),
    dcc.Graph(id="observer-graph", figure=get_3d_fig()),
    dcc.Graph(id="branch-graph", figure=get_branch_fig()),
    dbc.InputGroup([
        dbc.Input(id="command-input", placeholder="Enter observer command (e.g., 'merge conflicts')", type="text"),
        dbc.Button("Execute", id="run-command", n_clicks=0)
    ], className="mb-3"),
    html.Pre(id="log-output", children="", style={"whiteSpace": "pre-wrap"})
])

@app.callback(
    Output("observer-graph", "figure"),
    Output("branch-graph", "figure"),
    Output("log-output", "children"),
    Input("run-command", "n_clicks"),
    State("command-input", "value"),
    prevent_initial_call=True
)
def update_graph(n_clicks, command):
    global context
    try:
        result = engine.execute(command, context)
        if command.lower().startswith("merge"):
            context["nodes"] = result
        obs_fig = get_3d_fig()
        branch_fig = get_branch_fig()
        log = "\n".join(engine.log)
        return obs_fig, branch_fig, log
    except Exception as e:
        return dash.no_update, dash.no_update, f"Error: {str(e)}"

if __name__ == "__main__":
    app.run_server(debug=True)

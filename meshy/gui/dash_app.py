import sys
from pathlib import Path

# Add project root to sys.path for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from datetime import datetime
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

from agents.human_agent import HumanAgent
from agents.observer_entity import ObserverEntity
from agents.observer_script import ObserverScriptEngine
from visualization import render_observer_view, render_branch_graph

# --- Initialize agents and observer environment ---
agent_a = HumanAgent("agent_alpha")
agent_b = HumanAgent("agent_beta")

agent_a.perceive_event(
    t=datetime(1983, 7, 12, 12, 0),
    position=(0, 0, 0),
    event_data={"description": "Mandela funeral"}
)

agent_b.perceive_event(
    t=datetime(1983, 7, 12, 12, 0),
    position=(0, 0, 0),
    event_data={"description": "Mandela speech at UN"}
)

observer = ObserverEntity()
conflicts = observer.detect_conflicts([agent_a, agent_b])
engine = ObserverScriptEngine(observer)

context = {
    "conflicts": conflicts,
    "nodes": []
}

# --- Dash app setup ---
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Meshy Observer Console"

def get_3d_fig():
    return render_observer_view(agent_a.memory + agent_b.memory + context.get("nodes", []), return_fig=True)

def get_branch_fig():
    return render_branch_graph(agent_a.memory + agent_b.memory + context.get("nodes", []), return_fig=True)

app.layout = dbc.Container([
    html.H1("Meshy – Observer View", className="my-3"),
    dcc.Graph(id="observer-graph", figure=get_3d_fig()),
    dcc.Graph(id="branch-graph", figure=get_branch_fig()),
    dbc.InputGroup([
        dbc.Input(id="command-input", placeholder="Enter observer command (e.g., 'merge conflicts')", type="text"),
        dbc.Button("Execute", id="run-command", n_clicks=0)
    ], className="mb-3"),
    html.Pre(id="log-output", style={"whiteSpace": "pre-wrap", "backgroundColor": "#222", "padding": "1em", "borderRadius": "5px"})
])

@app.callback(
    Output("observer-graph", "figure"),
    Output("branch-graph", "figure"),
    Output("log-output", "children"),
    Input("run-command", "n_clicks"),
    State("command-input", "value"),
    prevent_initial_call=True
)
def handle_observer_command(n_clicks, command):
    global context
    try:
        result = engine.execute(command.strip(), context)
        if command.lower().startswith("merge"):
            context["nodes"] = result

        fig1 = get_3d_fig()
        fig2 = get_branch_fig()
        return fig1, fig2, "\n".join(engine.log)
    except Exception as e:
        return get_3d_fig(), get_branch_fig(), f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)

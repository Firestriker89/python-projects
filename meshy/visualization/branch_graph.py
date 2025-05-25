import os
import pandas as pd
import plotly.graph_objects as go
from timeline.node import TimelineNode
from typing import List

def render_branch_graph(nodes: List[TimelineNode], title="Branch Graph"):
    """
    Renders a Git-style commit graph showing parent-child relationships.
    """
    if not nodes:
        print("No nodes to graph.")
        return

    # Map nodes to a stable ID
    node_ids = {id(node): idx for idx, node in enumerate(nodes)}

    node_data = []
    edge_x = []
    edge_y = []
    texts = []

    for idx, node in enumerate(nodes):
        # Layout horizontally by time, vertically by branch
        x = node.t.timestamp()
        y = hash(node.branch_id) % 10  # crude vertical spacing

        node_data.append({
            "x": x,
            "y": y,
            "desc": node.event_data.get("description", "N/A"),
            "agent": node.agent_id,
            "branch": node.branch_id,
            "time": node.t.isoformat()
        })

        texts.append(f"{node.agent_id} [{node.branch_id}]<br>{node.event_data.get('description')}")

        for parent in node.parents:
            if id(parent) in node_ids:
                edge_x += [parent.t.timestamp(), x, None]
                edge_y += [hash(parent.branch_id) % 10, y, None]

    df = pd.DataFrame(node_data)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color="#888"),
        hoverinfo='none',
        mode='lines'
    )

    node_trace = go.Scatter(
        x=df["x"],
        y=df["y"],
        mode='markers+text',
        text=texts,
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            color=[hash(b) % 10 for b in df["branch"]],
            size=10,
            colorbar=dict(title="Branch ID")
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=title,
                        showlegend=False,
                        xaxis=dict(title='Time'),
                        yaxis=dict(title='Branch Space'),
                        hovermode='closest'
                    ))

    os.makedirs("output", exist_ok=True)
    fig.write_html("output/branch_graph.html", auto_open=True)

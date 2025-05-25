"""
Visualization stub for Meshy timeline density maps.

Planned:
- 3D position-time scatter plots
- Color by agent or branch
- Density over x/y/z/time voxels
"""

import plotly.express as px
import pandas as pd
from timeline.node import TimelineNode
from typing import List
import os

def render_timeline_nodes(nodes: List[TimelineNode], title="Timeline View 3D"):
    """
    Renders timeline nodes in 3D space with color-coded agents.
    Saves to an HTML file instead of attempting direct browser rendering.
    """
    if not nodes:
        print("No nodes to render.")
        return

    data = [{
        "x": node.position[0],
        "y": node.position[1],
        "z": node.position[2],
        "t": node.t.isoformat(),
        "agent": node.agent_id or "unknown",
        "desc": node.event_data.get("description", "N/A"),
        "branch": node.branch_id
    } for node in nodes]

    df = pd.DataFrame(data)

    fig = px.scatter_3d(
        df,
        x="x", y="y", z="z",
        color="agent",
        hover_data=["t", "desc", "branch"],
        title=title
    )

    output_path = os.path.join("output", "mesh_timeline.html")
    os.makedirs("output", exist_ok=True)
    fig.write_html(output_path, auto_open=True)

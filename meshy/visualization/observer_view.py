import os
import pandas as pd
import plotly.express as px
from typing import List
from timeline.node import TimelineNode

# Emotion → Color mapping
emotion_color_map = {
    "grief": "blue",
    "hope": "green",
    "confusion": "purple",
    "anger": "red",
    "joy": "gold",
    "fear": "orange",
    "neutral": "gray"
}

def render_observer_view(nodes: List[TimelineNode], title="Observer View", return_fig=False, color_by="emotion"):
    if not nodes:
        print("No nodes to render.")
        return None

    data = []
    for node in nodes:
        intent = node.intent_meta or {}
        emotion = intent.get("emotion", "neutral")
        certainty = intent.get("certainty", 0.5)

        data.append({
            "x": node.position[0],
            "y": node.position[1],
            "z": node.position[2],
            "time": node.t.isoformat(),
            "agent": node.agent_id or "unknown",
            "desc": node.event_data.get("description", "N/A"),
            "branch": node.branch_id,
            "emotion": emotion,
            "certainty": certainty,
            "color": emotion_color_map.get(emotion, "gray"),
            "size": max(5, certainty * 20)  # scale certainty to bubble size
        })

    df = pd.DataFrame(data)

    fig = px.scatter_3d(
        df,
        x="x", y="y", z="z",
        color="emotion",
        size="size",
        hover_data=["time", "desc", "agent", "branch", "certainty"],
        title=title
    )

    if return_fig:
        return fig
    else:
        os.makedirs("output", exist_ok=True)
        fig.write_html("output/observer_view.html", auto_open=True)

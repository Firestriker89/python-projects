# visualization/__init__.py

"""
Meshy Visualization Module

Contains utilities for rendering timeline nodes, observer perspectives,
and branching structure as 3D visualizations or directed graphs.
"""

# Optional: expose frequently used rendering functions
from .observer_view import render_observer_view
from .branch_graph import render_branch_graph
from .render_3d import render_timeline_nodes

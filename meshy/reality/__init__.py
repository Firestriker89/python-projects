"""
Reality Module

This module contains reality management classes for the Meshy system:
- ConflictResolver: Handles detection and resolution of conflicts
- FloorTag: Represents tagged timeline floors
"""

from .conflict_resolver import ConflictResolver
from .floor import FloorTag

__all__ = ["ConflictResolver", "FloorTag"]

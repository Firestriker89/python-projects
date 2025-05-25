"""
Global configuration for the Meshy simulator.
Modify values here to change simulation behavior across modules.
"""

# Conflict resolution strategy: 'merge', 'reject', 'split'
DEFAULT_RESOLUTION_STRATEGY = "merge"

# Logging verbosity: 'none', 'basic', 'verbose'
LOGGING_LEVEL = "basic"

# Minimum time granularity (seconds) for timeline analysis
TIME_SLICE_GRANULARITY = 1.0

# Future: resolution policies for different agent types
AGENT_POLICY = {
    "human": {"memory_cap": 1000},
    "observer": {"merge_threshold": 0.8},
}

# Visualization parameters (hook for future module)
VISUALIZATION_ENABLED = False
VISUALIZATION_DIMENSIONS = (10, 10, 3)  # x, y, z space

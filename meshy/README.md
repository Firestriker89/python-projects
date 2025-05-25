# Meshy

A Python framework for managing timelines, agents, and reality conflicts in complex systems.

## Overview

Meshy provides a comprehensive system for:
- **Timeline Management**: Node-based timeline system for tracking events and states
- **Agent System**: Extensible agent framework with human interaction capabilities  
- **Conflict Resolution**: Multiple strategies for handling conflicts and inconsistencies
- **Observer Pattern**: Monitoring and trigger system for system events
- **3D Visualization**: Interactive timeline and mesh rendering capabilities

## Project Structure

```
meshy/
├── agents/              # Agent system components
│   ├── base_agent.py   # Abstract base class for agents
│   ├── human_agent.py  # Human participant agents
│   └── observer_entity.py # Monitoring and observation agents
├── timeline/           # Timeline management
│   └── node.py        # Timeline node implementation
├── reality/           # Reality and conflict management
│   ├── conflict_resolver.py # Conflict detection and resolution
│   └── floor.py       # Timeline floor tagging system
├── visualization/     # Visualization components
│   ├── render_3d.py   # 3D rendering capabilities
│   └── observer_view.py # Observer-specific visualizations
├── output/           # Generated visualization files
├── config.py        # System configuration
├── main.py         # Main application entry point
└── requirements.txt # Python dependencies
```

## Getting Started

### Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Basic Usage

```python
from agents.human_agent import HumanAgent
from agents.observer_entity import ObserverEntity
from reality.conflict_resolver import ConflictResolver
from datetime import datetime

# Create agents
agent_a = HumanAgent("agent_alpha")
agent_b = HumanAgent("agent_beta")

# Have agents perceive events
agent_a.perceive_event(
    t=datetime(1983, 7, 12, 12, 0),
    position=(0, 0, 0),
    event_data={"description": "Event A"},
    intent_meta={"emotion": "neutral"}
)

# Detect and resolve conflicts
observer = ObserverEntity()
conflicts = observer.detect_conflicts([agent_a, agent_b])

resolver = ConflictResolver(strategy="merge")
resolved = resolver.resolve(conflicts)
```

### Running the Demo

```bash
python main.py
```

## Key Features

### Timeline Management
- Node-based timeline system
- Parent-child relationships between timeline events
- Temporal conflict detection and resolution

### Agent System
- Abstract base agent class for extensibility
- Human agents with console interaction
- Observer entities for monitoring system states
- Trigger-based event handling

### Conflict Resolution
- Multiple resolution strategies:
  - Priority-based resolution
  - Timestamp-based resolution
  - Consensus-based resolution
  - Majority rule
  - Manual review
- Configurable conflict detection

### Visualization
- 3D timeline rendering
- Interactive HTML output
- Observer monitoring dashboards
- Real-time visualization updates

## Configuration

The system can be configured through `config.py` or environment variables:

```python
# Example configuration
DEBUG = True
MAX_TIMELINE_DEPTH = 1000
DEFAULT_RESOLUTION_STRATEGY = "merge"
VISUALIZATION_PORT = 8080
```

## Development

### VS Code Setup
The project includes VS Code configuration with:
- Python linting and formatting (pylint, black)
- Recommended extensions
- Debug configurations

### Testing
```bash
pytest
```

### Code Formatting
```bash
black .
```

## Contributing

1. Follow the existing code structure and patterns
2. Add appropriate docstrings and type hints
3. Include tests for new functionality
4. Use black for code formatting

## License

[Add your license information here]

## Roadmap

- [ ] Enhanced 3D visualization capabilities
- [ ] Web-based interface
- [ ] Database persistence
- [ ] Advanced conflict resolution algorithms
- [ ] Multi-agent coordination protocols
- [ ] Real-time collaboration features

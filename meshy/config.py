"""
Configuration Module

This module contains configuration settings and utilities for the Meshy system.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    """
    Configuration class for the Meshy system.
    
    Contains all system-wide configuration parameters and settings.
    """
    
    # System settings
    debug: bool = False
    log_level: str = "INFO"
    max_timeline_depth: int = 1000
    
    # Agent settings
    default_agent_timeout: int = 30  # seconds
    max_agents: int = 100
    
    # Observer settings
    max_observations: int = 10000
    observation_retention_days: int = 30
    
    # Conflict resolver settings
    default_conflict_strategy: str = "priority_based"
    max_pending_conflicts: int = 50
    
    # File paths
    data_directory: str = field(default_factory=lambda: str(Path.cwd() / "data"))
    log_directory: str = field(default_factory=lambda: str(Path.cwd() / "logs"))
    config_file: str = field(default_factory=lambda: str(Path.cwd() / "meshy_config.json"))
    
    # Performance settings
    enable_caching: bool = True
    cache_size: int = 1000
    
    # Visualization settings
    enable_visualization: bool = False
    visualization_port: int = 8080
    
    def __post_init__(self):
        """Post-initialization to create directories and validate settings."""
        self._create_directories()
        self._validate_settings()
        self._load_environment_overrides()
        
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [self.data_directory, self.log_directory]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            
    def _validate_settings(self) -> None:
        """Validate configuration settings."""
        if self.max_timeline_depth <= 0:
            raise ValueError("max_timeline_depth must be positive")
            
        if self.max_agents <= 0:
            raise ValueError("max_agents must be positive")
            
        if self.max_observations <= 0:
            raise ValueError("max_observations must be positive")
            
    def _load_environment_overrides(self) -> None:
        """Load configuration overrides from environment variables."""
        env_mappings = {
            "MESHY_DEBUG": ("debug", bool),
            "MESHY_LOG_LEVEL": ("log_level", str),
            "MESHY_MAX_AGENTS": ("max_agents", int),
            "MESHY_DATA_DIR": ("data_directory", str),
            "MESHY_LOG_DIR": ("log_directory", str),
            "MESHY_ENABLE_CACHE": ("enable_caching", bool),
            "MESHY_VIZ_PORT": ("visualization_port", int),
        }
        
        for env_var, (attr_name, attr_type) in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                try:
                    if attr_type == bool:
                        setattr(self, attr_name, env_value.lower() in ('true', '1', 'yes', 'on'))
                    else:
                        setattr(self, attr_name, attr_type(env_value))
                except (ValueError, TypeError) as e:
                    print(f"Warning: Invalid value for {env_var}: {env_value}. Error: {e}")
                    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "debug": self.debug,
            "log_level": self.log_level,
            "max_timeline_depth": self.max_timeline_depth,
            "default_agent_timeout": self.default_agent_timeout,
            "max_agents": self.max_agents,
            "max_observations": self.max_observations,
            "observation_retention_days": self.observation_retention_days,
            "default_conflict_strategy": self.default_conflict_strategy,
            "max_pending_conflicts": self.max_pending_conflicts,
            "data_directory": self.data_directory,
            "log_directory": self.log_directory,
            "config_file": self.config_file,
            "enable_caching": self.enable_caching,
            "cache_size": self.cache_size,
            "enable_visualization": self.enable_visualization,
            "visualization_port": self.visualization_port
        }
        
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """Create configuration from dictionary."""
        return cls(**config_dict)
        
    def update(self, **kwargs) -> None:
        """Update configuration with new values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: Unknown configuration key: {key}")
                
    def get_database_url(self) -> Optional[str]:
        """Get database URL from environment or return None."""
        return os.getenv("MESHY_DATABASE_URL")
        
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service."""
        env_var = f"MESHY_{service.upper()}_API_KEY"
        return os.getenv(env_var)
        
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return os.getenv("MESHY_ENV", "development").lower() == "production"
        
    def __repr__(self) -> str:
        return f"Config(debug={self.debug}, log_level={self.log_level}, max_agents={self.max_agents})"

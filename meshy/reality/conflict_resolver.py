"""
Conflict Resolver Module

This module contains the ConflictResolver class for handling conflicts and inconsistencies.
"""

from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class ConflictType(Enum):
    """Enumeration of different conflict types."""
    STATE_CONFLICT = "state_conflict"
    TEMPORAL_CONFLICT = "temporal_conflict"
    AGENT_CONFLICT = "agent_conflict"
    RESOURCE_CONFLICT = "resource_conflict"
    LOGICAL_CONFLICT = "logical_conflict"


class ConflictResolutionStrategy(Enum):
    """Enumeration of conflict resolution strategies."""
    PRIORITY_BASED = "priority_based"
    TIMESTAMP_BASED = "timestamp_based"
    CONSENSUS_BASED = "consensus_based"
    MAJORITY_RULE = "majority_rule"
    MANUAL_REVIEW = "manual_review"


class ConflictResolver:
    """
    Handles detection and resolution of conflicts in the system.
    
    Can detect various types of conflicts and apply different resolution
    strategies based on the conflict type and system configuration.
    """
    
    def __init__(self, default_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.PRIORITY_BASED):
        self.default_strategy = default_strategy
        self.resolution_strategies = {}
        self.conflict_history = []
        self.pending_conflicts = []
        
        # Set up default resolution strategies
        self._initialize_strategies()
        
    def detect_conflicts(self, states: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect conflicts between different states or data.
        
        Args:
            states: List of state dictionaries to check for conflicts
            
        Returns:
            List of detected conflicts
        """
        conflicts = []
        
        for i, state1 in enumerate(states):
            for j, state2 in enumerate(states[i+1:], i+1):
                conflict = self._check_state_conflict(state1, state2, i, j)
                if conflict:
                    conflicts.append(conflict)
                    
        return conflicts
        
    def resolve_conflict(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve a single conflict using the appropriate strategy.
        
        Args:
            conflict: Conflict dictionary containing conflict information
            
        Returns:
            Resolution result
        """
        conflict_type = ConflictType(conflict.get("type", ConflictType.STATE_CONFLICT.value))
        strategy = self.resolution_strategies.get(conflict_type, self.default_strategy)
        
        resolution = {
            "conflict_id": conflict.get("id"),
            "timestamp": datetime.now(),
            "strategy_used": strategy.value,
            "original_conflict": conflict,
            "resolution": None,
            "success": False
        }
        
        try:
            if strategy == ConflictResolutionStrategy.PRIORITY_BASED:
                resolution["resolution"] = self._resolve_by_priority(conflict)
            elif strategy == ConflictResolutionStrategy.TIMESTAMP_BASED:
                resolution["resolution"] = self._resolve_by_timestamp(conflict)
            elif strategy == ConflictResolutionStrategy.CONSENSUS_BASED:
                resolution["resolution"] = self._resolve_by_consensus(conflict)
            elif strategy == ConflictResolutionStrategy.MAJORITY_RULE:
                resolution["resolution"] = self._resolve_by_majority(conflict)
            else:
                resolution["resolution"] = self._mark_for_manual_review(conflict)
                
            resolution["success"] = True
            
        except Exception as e:
            resolution["error"] = str(e)
            resolution["success"] = False
            
        self.conflict_history.append(resolution)
        return resolution
        
    def resolve_all_conflicts(self, conflicts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Resolve multiple conflicts.
        
        Args:
            conflicts: List of conflicts to resolve
            
        Returns:
            List of resolution results
        """
        resolutions = []
        for conflict in conflicts:
            resolution = self.resolve_conflict(conflict)
            resolutions.append(resolution)
            
        return resolutions
        
    def set_strategy(self, conflict_type: ConflictType, strategy: ConflictResolutionStrategy) -> None:
        """Set resolution strategy for a specific conflict type."""
        self.resolution_strategies[conflict_type] = strategy
        
    def get_conflict_statistics(self) -> Dict[str, Any]:
        """Get statistics about conflict resolution."""
        total_conflicts = len(self.conflict_history)
        successful_resolutions = sum(1 for r in self.conflict_history if r["success"])
        
        return {
            "total_conflicts": total_conflicts,
            "successful_resolutions": successful_resolutions,
            "success_rate": successful_resolutions / total_conflicts if total_conflicts > 0 else 0,
            "pending_conflicts": len(self.pending_conflicts),
            "strategies_used": list(set(r["strategy_used"] for r in self.conflict_history))
        }
        
    def _initialize_strategies(self) -> None:
        """Initialize default resolution strategies for different conflict types."""
        self.resolution_strategies = {
            ConflictType.STATE_CONFLICT: ConflictResolutionStrategy.TIMESTAMP_BASED,
            ConflictType.TEMPORAL_CONFLICT: ConflictResolutionStrategy.TIMESTAMP_BASED,
            ConflictType.AGENT_CONFLICT: ConflictResolutionStrategy.PRIORITY_BASED,
            ConflictType.RESOURCE_CONFLICT: ConflictResolutionStrategy.MAJORITY_RULE,
            ConflictType.LOGICAL_CONFLICT: ConflictResolutionStrategy.MANUAL_REVIEW
        }
        
    def _check_state_conflict(self, state1: Dict[str, Any], state2: Dict[str, Any], 
                             index1: int, index2: int) -> Optional[Dict[str, Any]]:
        """Check if two states conflict with each other."""
        # Simple conflict detection - look for same keys with different values
        conflicting_keys = []
        
        for key in state1.keys():
            if key in state2 and state1[key] != state2[key]:
                conflicting_keys.append(key)
                
        if conflicting_keys:
            return {
                "id": f"conflict_{index1}_{index2}_{datetime.now().timestamp()}",
                "type": ConflictType.STATE_CONFLICT.value,
                "conflicting_keys": conflicting_keys,
                "state1": state1,
                "state2": state2,
                "detected_at": datetime.now()
            }
            
        return None
        
    def _resolve_by_priority(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflict based on priority."""
        state1 = conflict["state1"]
        state2 = conflict["state2"]
        
        # Use priority if available, otherwise default to state1
        priority1 = state1.get("priority", 0)
        priority2 = state2.get("priority", 0)
        
        if priority1 >= priority2:
            return {"resolved_state": state1, "reason": "higher_priority"}
        else:
            return {"resolved_state": state2, "reason": "higher_priority"}
            
    def _resolve_by_timestamp(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflict based on timestamp (latest wins)."""
        state1 = conflict["state1"]
        state2 = conflict["state2"]
        
        timestamp1 = state1.get("timestamp", datetime.min)
        timestamp2 = state2.get("timestamp", datetime.min)
        
        if timestamp1 >= timestamp2:
            return {"resolved_state": state1, "reason": "more_recent"}
        else:
            return {"resolved_state": state2, "reason": "more_recent"}
            
    def _resolve_by_consensus(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflict based on consensus (simplified)."""
        # For now, just return the first state as a placeholder
        return {"resolved_state": conflict["state1"], "reason": "consensus_placeholder"}
        
    def _resolve_by_majority(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflict based on majority rule (simplified)."""
        # For now, just return the first state as a placeholder
        return {"resolved_state": conflict["state1"], "reason": "majority_placeholder"}
        
    def _mark_for_manual_review(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """Mark conflict for manual review."""
        self.pending_conflicts.append(conflict)
        return {"resolved_state": None, "reason": "marked_for_manual_review"}

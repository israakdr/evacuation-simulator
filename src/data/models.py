"""
Data models for the Evacuation Simulator.

This module defines the core data structures:
- Point: a 2D coordinate
- Wall: a wall segment
- Room: a room with walls and exits
- Exit: an exit point
- Building: the complete building
"""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Point:
    """A 2D point in the floorplan."""
    x: float
    y: float


@dataclass
class Wall:
    """A wall segment defined by two points."""
    start: Point
    end: Point


@dataclass
class Exit:
    """An exit point in the building."""
    id: int
    position: Point
    width: float = 1.0  # Exit width in meters


@dataclass
class Room:
    """A room in the building."""
    id: int
    name: str
    walls: List[Wall] = field(default_factory=list)
    area: float = 0.0  # Area in square meters
    capacity: int = 0  # Maximum number of people


@dataclass
class Building:
    """The complete building model."""
    name: str
    width: float          # Width in meters
    height: float         # Height in meters
    rooms: List[Room] = field(default_factory=list)
    exits: List[Exit] = field(default_factory=list)
    walls: List[Wall] = field(default_factory=list)
    
    def total_capacity(self) -> int:
        """Return the total capacity of the building."""
        return sum(room.capacity for room in self.rooms)
    
    def total_exits(self) -> int:
        """Return the total number of exits."""
        return len(self.exits)

"""
Scenario Builder for LaCAM0

Creates .scen files compatible with the LaCAM0 solver format.
Format: version 1
Each line: bucket map_name width height start_x start_y goal_x goal_y optimal_length
"""

from pathlib import Path
from typing import List, Tuple, Optional
import math


class ScenarioBuilder:
    """Builder for creating .scen scenario files for MAPF problems."""
    
    def __init__(self, map_name: str, width: int, height: int):
        """
        Initialize the scenario builder.
        
        Args:
            map_name: Name of the map file (e.g., "random-32-32-10.map")
            width: Width of the map
            height: Height of the map
        """
        self.map_name = map_name
        self.width = width
        self.height = height
        self.agents: List[Tuple[int, int, int, int, int, float]] = []  # bucket, start_x, start_y, goal_x, goal_y, optimal_length
    
    def add_agent(self, start_x: int, start_y: int, goal_x: int, goal_y: int, 
                  bucket: int = 1, optimal_length: Optional[float] = None):
        """
        Add an agent to the scenario.
        
        Args:
            start_x: Starting x coordinate
            start_y: Starting y coordinate
            goal_x: Goal x coordinate
            goal_y: Goal y coordinate
            bucket: Bucket number (default: 1)
            optimal_length: Optimal path length (if None, calculates Euclidean distance)
        """
        if not (0 <= start_x < self.width and 0 <= start_y < self.height):
            raise ValueError(f"Start position ({start_x}, {start_y}) out of bounds")
        
        if not (0 <= goal_x < self.width and 0 <= goal_y < self.height):
            raise ValueError(f"Goal position ({goal_x}, {goal_y}) out of bounds")
        
        if optimal_length is None:
            # Calculate Euclidean distance as optimal length
            optimal_length = math.sqrt((goal_x - start_x) ** 2 + (goal_y - start_y) ** 2)
        
        self.agents.append((bucket, start_x, start_y, goal_x, goal_y, optimal_length))
    
    def add_agents_from_list(self, agents: List[Tuple[int, int, int, int]], bucket: int = 1):
        """
        Add multiple agents from a list.
        
        Args:
            agents: List of tuples (start_x, start_y, goal_x, goal_y)
            bucket: Bucket number for all agents (default: 1)
        """
        for start_x, start_y, goal_x, goal_y in agents:
            self.add_agent(start_x, start_y, goal_x, goal_y, bucket)
    
    def clear(self):
        """Clear all agents from the scenario."""
        self.agents = []
    
    def build(self) -> str:
        """
        Build the scenario file content as a string.
        
        Returns:
            String containing the .scen file content
        """
        lines = ["version 1"]
        
        for bucket, start_x, start_y, goal_x, goal_y, optimal_length in self.agents:
            line = f"{bucket}\t{self.map_name}\t{self.width}\t{self.height}\t{start_x}\t{start_y}\t{goal_x}\t{goal_y}\t{optimal_length:.8f}"
            lines.append(line)
        
        return "\n".join(lines) + "\n"
    
    def save(self, output_path: str):
        """
        Save the scenario to a .scen file.
        
        Args:
            output_path: Path to save the .scen file
        """
        content = self.build()
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(content)
    
    def __len__(self):
        """Return the number of agents in the scenario."""
        return len(self.agents)


def load_scenario(scenario_path: str) -> ScenarioBuilder:
    """
    Load an existing .scen file into a ScenarioBuilder.
    
    Args:
        scenario_path: Path to the .scen file
        
    Returns:
        ScenarioBuilder instance with loaded data
    """
    with open(scenario_path, 'r') as f:
        lines = f.readlines()
    
    if not lines or not lines[0].strip().startswith("version"):
        raise ValueError("Invalid scenario file format")
    
    # Parse first agent line to get map info
    first_line = lines[1].strip().split('\t')
    map_name = first_line[1]
    width = int(first_line[2])
    height = int(first_line[3])
    
    builder = ScenarioBuilder(map_name, width, height)
    
    # Parse all agent lines
    for line in lines[1:]:
        parts = line.strip().split('\t')
        if len(parts) >= 8:
            bucket = int(parts[0])
            start_x = int(parts[4])
            start_y = int(parts[5])
            goal_x = int(parts[6])
            goal_y = int(parts[7])
            optimal_length = float(parts[8]) if len(parts) > 8 else None
            
            builder.add_agent(start_x, start_y, goal_x, goal_y, bucket, optimal_length)
    
    return builder


if __name__ == "__main__":
    # Example 1: Create a simple scenario
    builder = ScenarioBuilder("random-32-32-10.map", 32, 32)
    
    # Add some agents
    builder.add_agent(11, 6, 7, 18, bucket=3)
    builder.add_agent(29, 9, 1, 16, bucket=7)
    builder.add_agent(9, 0, 13, 21, bucket=5)
    
    # Save to file
    output_dir = Path(__file__).parent.parent.parent / "cpp" / "lacam0" / "assets"
    builder.save(str(output_dir / "example_scenario.scen"))
    
    print(f"Created scenario with {len(builder)} agents")
    
    # Example 2: Load existing scenario and modify
    existing_scen = output_dir / "random-32-32-10-random-1.scen"
    if existing_scen.exists():
        loaded = load_scenario(str(existing_scen))
        print(f"Loaded scenario with {len(loaded)} agents")

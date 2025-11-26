"""
Result Reader for LaCAM0

Loads and parses result files from the LaCAM0 solver output format.
"""

from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class LaCAM0Result:
    """Data structure for LaCAM0 solver results."""
    
    # Basic info
    agents: int
    map_file: str
    solver: str
    solved: bool
    
    # Performance metrics
    sum_of_costs: int
    sum_of_costs_lb: int
    makespan: int
    makespan_lb: int
    sum_of_loss: int
    sum_of_loss_lb: int
    comp_time: int  # in milliseconds
    seed: int
    
    # Agent data
    starts: List[Tuple[int, int]]
    goals: List[Tuple[int, int]]
    
    # Solution paths
    solution: List[List[Tuple[int, int]]]  # timestep -> list of agent positions
    
    @property
    def num_timesteps(self) -> int:
        """Return the number of timesteps in the solution."""
        return len(self.solution)
    
    @property
    def is_optimal_soc(self) -> bool:
        """Check if the solution has optimal sum of costs."""
        return self.sum_of_costs == self.sum_of_costs_lb
    
    @property
    def is_optimal_makespan(self) -> bool:
        """Check if the solution has optimal makespan."""
        return self.makespan == self.makespan_lb
    
    def get_agent_path(self, agent_id: int) -> List[Tuple[int, int]]:
        """
        Get the complete path for a specific agent.
        
        Args:
            agent_id: Index of the agent (0-based)
            
        Returns:
            List of (x, y) positions for each timestep
        """
        if agent_id < 0 or agent_id >= self.agents:
            raise ValueError(f"Agent ID {agent_id} out of range [0, {self.agents})")
        
        return [timestep[agent_id] for timestep in self.solution]
    
    def get_agent_path_length(self, agent_id: int) -> int:
        """
        Calculate the path length for a specific agent (excluding wait actions at goal).
        
        Args:
            agent_id: Index of the agent (0-based)
            
        Returns:
            Number of moves (non-wait actions)
        """
        path = self.get_agent_path(agent_id)
        goal = self.goals[agent_id]
        
        # Find first timestep when agent reaches goal
        for i, pos in enumerate(path):
            if pos == goal:
                return i
        
        return len(path) - 1
    
    def __str__(self) -> str:
        """String representation of the result."""
        status = "SOLVED" if self.solved else "UNSOLVED"
        optimal = " (OPTIMAL)" if self.is_optimal_soc else " (SUBOPTIMAL)"
        
        return (
            f"LaCAM0 Result: {status}{optimal if self.solved else ''}\n"
            f"  Agents: {self.agents}\n"
            f"  Map: {self.map_file}\n"
            f"  Sum of Costs: {self.sum_of_costs} (lb={self.sum_of_costs_lb})\n"
            f"  Makespan: {self.makespan} (lb={self.makespan_lb})\n"
            f"  Computation Time: {self.comp_time}ms\n"
            f"  Solution Length: {self.num_timesteps} timesteps"
        )


def parse_coord_list(coord_str: str) -> List[Tuple[int, int]]:
    """
    Parse a comma-separated list of coordinates.
    
    Args:
        coord_str: String like "(11,6),(29,9),(9,0),"
        
    Returns:
        List of (x, y) tuples
    """
    coords = []
    # Remove trailing comma and split
    parts = coord_str.rstrip(',').split('),(')
    
    for part in parts:
        # Clean up parentheses
        clean = part.strip('()')
        if clean:
            x, y = map(int, clean.split(','))
            coords.append((x, y))
    
    return coords


def load_result(result_path: str) -> LaCAM0Result:
    """
    Load a LaCAM0 result file.
    
    Args:
        result_path: Path to the result file
        
    Returns:
        LaCAM0Result object with parsed data
        
    Raises:
        FileNotFoundError: If the result file doesn't exist
        ValueError: If the file format is invalid
    """
    result_file = Path(result_path)
    
    if not result_file.exists():
        raise FileNotFoundError(f"Result file not found: {result_path}")
    
    with open(result_file, 'r') as f:
        lines = f.readlines()
    
    # Parse header fields
    data = {}
    solution_start_idx = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        if line.startswith('solution='):
            solution_start_idx = i + 1
            break
        
        if '=' in line:
            key, value = line.split('=', 1)
            data[key] = value
    
    # Parse basic fields
    agents = int(data['agents'])
    map_file = data['map_file']
    solver = data['solver']
    solved = bool(int(data['solved']))
    
    # Parse metrics
    soc = int(data['soc'])
    soc_lb = int(data['soc_lb'])
    makespan = int(data['makespan'])
    makespan_lb = int(data['makespan_lb'])
    sum_of_loss = int(data['sum_of_loss'])
    sum_of_loss_lb = int(data['sum_of_loss_lb'])
    comp_time = int(data['comp_time'])
    seed = int(data['seed'])
    
    # Parse starts and goals
    starts = parse_coord_list(data['starts'])
    goals = parse_coord_list(data['goals'])
    
    # Parse solution
    solution = []
    
    if solution_start_idx is not None:
        for line in lines[solution_start_idx:]:
            line = line.strip()
            if not line:
                continue
            
            # Format: "0:(11,6),(29,9),(9,0),..."
            if ':' in line:
                timestep_str, coords_str = line.split(':', 1)
                timestep = int(timestep_str)
                coords = parse_coord_list(coords_str)
                solution.append(coords)
    
    return LaCAM0Result(
        agents=agents,
        map_file=map_file,
        solver=solver,
        solved=solved,
        sum_of_costs=soc,
        sum_of_costs_lb=soc_lb,
        makespan=makespan,
        makespan_lb=makespan_lb,
        sum_of_loss=sum_of_loss,
        sum_of_loss_lb=sum_of_loss_lb,
        comp_time=comp_time,
        seed=seed,
        starts=starts,
        goals=goals,
        solution=solution
    )


if __name__ == "__main__":
    # Example usage
    result_file = Path(__file__).parent.parent.parent / "cpp" / "lacam0" / "test_output.txt"
    
    if result_file.exists():
        result = load_result(str(result_file))
        print(result)
        print(f"\nAgent 0 path length: {result.get_agent_path_length(0)}")
        print(f"Agent 0 path (first 5 steps): {result.get_agent_path(0)[:5]}")
    else:
        print(f"Result file not found: {result_file}")
        print("Run the solver first to generate output.")

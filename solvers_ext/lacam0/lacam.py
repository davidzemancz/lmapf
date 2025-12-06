import subprocess
import os
from pathlib import Path


class LaCAM0Solver:
    """Wrapper for the LaCAM0 C++ solver."""
    
    def __init__(self):
        self.solver_dir = Path(__file__).parent.parent.parent / "cpp" / "lacam0"
        self.executable = self.solver_dir / "main"
    
    def run(self, scenario_file: str, map_file: str, num_agents: int = 400, verbose: int = 3) -> subprocess.CompletedProcess:
        """
        Run the LaCAM0 solver with the specified parameters.
        
        Args:
            scenario_file: Path to the scenario file (relative to solver assets or absolute)
            map_file: Path to the map file (relative to solver assets or absolute)
            num_agents: Number of agents (-N parameter)
            verbose: Verbosity level (-v parameter)
            
        Returns:
            CompletedProcess object with the result
            
        Raises:
            FileNotFoundError: If the executable or input files don't exist
        """
        if not self.executable.exists():
            raise FileNotFoundError(f"LaCAM0 executable not found at {self.executable}")
        
        # Resolve paths
        if not os.path.isabs(scenario_file):
            scenario_path = self.solver_dir / scenario_file
        else:
            scenario_path = Path(scenario_file)
            
        if not os.path.isabs(map_file):
            map_path = self.solver_dir / map_file
        else:
            map_path = Path(map_file)
        
        if not scenario_path.exists():
            raise FileNotFoundError(f"Scenario file not found at {scenario_path}")
        
        if not map_path.exists():
            raise FileNotFoundError(f"Map file not found at {map_path}")
        
        # Build command
        cmd = [
            str(self.executable),
            "-i", str(scenario_path),
            "-m", str(map_path),
            "-N", str(num_agents),
            "-v", str(verbose)
        ]
        
        # Run the command
        result = subprocess.run(
            cmd,
            cwd=str(self.solver_dir),
            capture_output=True,
            text=True
        )
        
        return result


if __name__ == "__main__":
    # Example usage
    solver = LaCAM0Solver()
    result = solver.run(
        scenario_file="assets/random-32-32-10-random-1.scen",
        map_file="assets/random-32-32-10.map",
        num_agents=400,
        verbose=3
    )
    
    print("STDOUT:")
    print(result.stdout)
    print("\nSTDERR:")
    print(result.stderr)
    print(f"\nReturn code: {result.returncode}")

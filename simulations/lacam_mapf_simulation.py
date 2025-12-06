import numpy as np

from solvers.pylacam.lacam import LaCAM
from solvers.pylacam.mapf_utils import LacamConfig, LacamGrid

from models.task import Task
from models.agent import Agent
from models.layout import Layout
from models.simulation import SimulationBase
from models.config import Config


class PylacamMAPFSimulation(SimulationBase):
    """Simulation that uses the pylacam solver to compute paths for all agents."""

    def __init__(self, layout: Layout, agents: list[Agent], tasks: list[Task]):
        super().__init__(layout, agents, tasks)
        self.solution: list[Config] = []
        self.current_step = 0
        self.solved = False

    def _layout_to_grid(self) -> LacamGrid:
        """Convert Layout to numpy grid for pylacam solver.

        Grid format: grid[y, x] -> True: available, False: obstacle
        """
        grid = np.zeros((self.layout.height, self.layout.width), dtype=bool)
        traversable = Layout.traversable_cells()
        for y in range(self.layout.height):
            for x in range(self.layout.width):
                grid[y, x] = self.layout.grid[y][x] in traversable
        return grid

    def _get_starts_config(self) -> LacamConfig:
        """Get starting positions of all agents as Config."""
        config = LacamConfig()
        for agent in self.agents:
            config.append((agent.y, agent.x))  # pylacam uses (y, x) format
        return config

    def _get_goals_config(self) -> LacamConfig:
        """Get goal positions (task locations) for all agents as Config."""
        config = LacamConfig()
        for agent in self.agents:
            if agent.task is not None:
                config.append((agent.task.y, agent.task.x))  # pylacam uses (y, x) format
            else:
                # If no task, agent stays at current position
                config.append((agent.y, agent.x))
        return config

    def solve(self, time_limit_ms: int = 3000, verbose: int = 0) -> bool:
        """Solve the MAPF instance for all agents.

        Args:
            time_limit_ms: Time limit for solver in milliseconds
            verbose: Verbosity level (0=silent, 1=basic, 2=detailed)

        Returns:
            True if solution found, False otherwise
        """
        grid = self._layout_to_grid()
        starts = self._get_starts_config()
        goals = self._get_goals_config()

        solver = LaCAM()
        lacam_solution = solver.solve(
            grid=grid,
            starts=starts,
            goals=goals,
            time_limit_ms=time_limit_ms,
            verbose=verbose
        )

        # Convert LacamConfig (y, x) to Config (x, y)
        self.solution = []
        for lacam_config in lacam_solution:
            config = Config()
            for y, x in lacam_config.positions:
                config.append((x, y))
            self.solution.append(config)

        self.solved = len(self.solution) > 0
        self.current_step = 0
        return self.solved

    def step(self) -> list[tuple[int, int]] | None:
        """Perform a simulation step, returning next positions for all agents.

        Returns:
            List of (x, y) positions for each agent, or None if no more steps
        """
        if not self.solved or self.current_step >= len(self.solution):
            return None

        config = self.solution[self.current_step]

        # Update agent positions
        for i, agent in enumerate(self.agents):
            agent.x, agent.y = config[i]

        self.current_step += 1
        return config.positions

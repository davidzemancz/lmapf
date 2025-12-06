import random

import numpy as np

from solvers_ext.pypibt.dist_table import PibtDistTable
from solvers_ext.pypibt.mapf_utils import PibtGrid, PibtCoord

from models.simulation import SimulationBase
from models.task import Task
from models.agent import Agent
from models.layout import Layout


class PIBTMAPDSimulation(SimulationBase):
    """PIBT-based MAPD (Multi-Agent Pickup and Delivery) simulation.

    This simulation uses PIBT for collision-free path planning while handling
    task assignment for pickup and delivery operations. Each step:
    1. Assigns unassigned tasks to free agents (greedy by distance)
    2. Plans one step using PIBT
    3. Updates agent positions and task states
    """

    grid: PibtGrid
    dist_tables: dict[PibtCoord, PibtDistTable]
    occupied_now: np.ndarray
    occupied_nxt: np.ndarray
    NIL: int
    NIL_COORD: PibtCoord
    rng: random.Random

    def __init__(self, layout: Layout, agents: list[Agent], tasks: list[Task], seed: int = 0):
        super().__init__(layout, agents, tasks)

        self.grid = self._layout_to_grid()
        self.rng = random.Random(seed)

        # Sentinel values
        self.NIL = len(agents)
        self.NIL_COORD = self.grid.shape

        # Occupation tracking
        self.occupied_now = np.full(self.grid.shape, self.NIL, dtype=int)
        self.occupied_nxt = np.full(self.grid.shape, self.NIL, dtype=int)

        # Distance table cache (lazily populated)
        self.dist_tables = {}

        # Initialize agents for PIBT
        for agent in agents:
            agent.goal_x = agent.x
            agent.goal_y = agent.y
            agent.elapsed = 0
            agent.tie_breaker = self.rng.random()
            agent.task = None
            agent.target_task = None
            self.occupied_now[agent.y, agent.x] = agent.id

    def _layout_to_grid(self) -> PibtGrid:
        """Convert Layout to numpy grid for PIBT.

        Grid format: grid[y, x] -> True: available, False: obstacle
        """
        grid = np.zeros((self.layout.height, self.layout.width), dtype=bool)
        traversable = Layout.traversable_cells()
        for y in range(self.layout.height):
            for x in range(self.layout.width):
                grid[y, x] = self.layout.grid[y][x] in traversable
        return grid

    def _get_dist_table(self, goal: PibtCoord) -> PibtDistTable:
        """Get or create distance table for a goal position."""
        if goal not in self.dist_tables:
            self.dist_tables[goal] = PibtDistTable(self.grid, goal)
        return self.dist_tables[goal]

    def _path_dist(self, start: PibtCoord, goal: PibtCoord) -> int:
        """Get shortest path distance from start to goal."""
        return self._get_dist_table(goal).get(start)

    def _get_neighbors(self, coord: PibtCoord) -> list[PibtCoord]:
        """Get valid neighboring coordinates (4-connected grid)."""
        y, x = coord
        neighbors = []

        if x > 0 and self.grid[y, x - 1]:
            neighbors.append((y, x - 1))
        if x < self.grid.shape[1] - 1 and self.grid[y, x + 1]:
            neighbors.append((y, x + 1))
        if y > 0 and self.grid[y - 1, x]:
            neighbors.append((y - 1, x))
        if y < self.grid.shape[0] - 1 and self.grid[y + 1, x]:
            neighbors.append((y + 1, x))

        return neighbors

    def _assign_task(self, agent: Agent, task: Task) -> None:
        """Assign a task to an agent (agent has reached pickup location)."""
        agent.task = task
        agent.target_task = None
        task.status = Task.STATUS_DELIVERING
        # Update goal to delivery location
        agent.goal_y = task.delivery_y
        agent.goal_x = task.delivery_x

    def _func_pibt(self, Q_from: list[PibtCoord], Q_to: list[PibtCoord], i: int) -> bool:
        """Core PIBT function for single agent planning with priority inheritance.

        Args:
            Q_from: Current configuration (positions at current timestep).
            Q_to: Next configuration being constructed (modified in-place).
            i: Agent index to plan for.

        Returns:
            True if successfully assigned a position to agent i, False otherwise.
        """
        agent = self.agents[i]
        goal = (agent.goal_y, agent.goal_x)

        # Compare function for sorting candidates
        def compare_key(v: PibtCoord) -> tuple[int, int, float]:
            d = self._path_dist(v, goal)
            # Prefer unoccupied cells (occupied_now check)
            occupied = 0 if self.occupied_now[v] == self.NIL else 1
            return (d, occupied, self.rng.random())

        # Get candidates: current position + neighbors
        C = [Q_from[i]] + self._get_neighbors(Q_from[i])
        self.rng.shuffle(C)
        C = sorted(C, key=compare_key)

        for v in C:
            # Avoid vertex collision
            if self.occupied_nxt[v] != self.NIL:
                continue

            j = self.occupied_now[v]

            # Avoid edge collision (swap)
            if j != self.NIL and j != i and Q_to[j] == Q_from[i]:
                continue

            # Reserve next location
            Q_to[i] = v
            self.occupied_nxt[v] = i

            # Priority inheritance
            if j != self.NIL and j != i and Q_to[j] == self.NIL_COORD:
                if not self._func_pibt(Q_from, Q_to, j):
                    continue

            return True

        # Failed to secure node - stay in place
        Q_to[i] = Q_from[i]
        self.occupied_nxt[Q_from[i]] = i
        return False

    def step(self) -> list[tuple[int, int]] | None:
        """Perform one simulation step.

        Returns:
            List of (x, y) positions for each agent after this step.
        """
        # 1. Task assignment phase
        # Get tasks that are already being targeted by other agents
        targeted_tasks = [a.target_task for a in self.agents if a.target_task is not None]
        unassigned_tasks = [t for t in self.tasks if t.status == Task.STATUS_PENDING and t not in targeted_tasks]
        self.rng.shuffle(unassigned_tasks)

        for agent in self.agents:
            # Agent already has an assigned task (delivering)
            if agent.task is not None:
                continue

            # Agent already targeting a task that's still pending - keep targeting it
            if agent.target_task is not None and agent.target_task.status == Task.STATUS_PENDING:
                continue

            # Free agent - find closest pickup location
            agent.target_task = None
            agent.goal_x = agent.x
            agent.goal_y = agent.y
            min_dist = self.grid.size
            best_task = None

            for task in unassigned_tasks:
                pickup_pos = (task.y, task.x)
                agent_pos = (agent.y, agent.x)
                d = self._path_dist(agent_pos, pickup_pos)

                if d == 0:
                    # Agent is at pickup location - assign immediately
                    self._assign_task(agent, task)
                    unassigned_tasks.remove(task)
                    best_task = None
                    break

                if d < min_dist:
                    min_dist = d
                    best_task = task

            # Target the best task found (and remove from available pool)
            if best_task is not None:
                agent.goal_x = best_task.x
                agent.goal_y = best_task.y
                agent.target_task = best_task
                unassigned_tasks.remove(best_task)

        # 2. Planning phase using PIBT
        # Sort agents by priority
        def priority_key(a: Agent) -> tuple[int, int, float]:
            has_task = 0 if a.task is not None else 1  # agents with tasks first
            return (has_task, -a.elapsed, -a.tie_breaker)

        sorted_agents = sorted(self.agents, key=priority_key)

        # Setup configurations
        Q_from = [(a.y, a.x) for a in self.agents]
        Q_to: list[PibtCoord] = [self.NIL_COORD] * len(self.agents)

        # Setup occupied_now
        for i, pos in enumerate(Q_from):
            self.occupied_now[pos] = i

        # Run PIBT for each agent in priority order
        for agent in sorted_agents:
            if Q_to[agent.id] == self.NIL_COORD:
                self._func_pibt(Q_from, Q_to, agent.id)

        # 3. Acting phase - update positions and states
        positions = []

        for agent in self.agents:
            v_now = (agent.y, agent.x)
            v_next = Q_to[agent.id]

            # Clear occupation
            if self.occupied_now[v_now] == agent.id:
                self.occupied_now[v_now] = self.NIL
            self.occupied_nxt[v_next] = self.NIL

            # Update position
            self.occupied_now[v_next] = agent.id

            # Update priority
            goal = (agent.goal_y, agent.goal_x)
            agent.elapsed = 0 if v_next == goal else agent.elapsed + 1

            # Update agent position
            agent.y, agent.x = v_next
            positions.append((agent.x, agent.y))

            # Update task info
            if agent.task is not None:
                # Check if delivery is complete
                delivery_pos = (agent.task.delivery_y, agent.task.delivery_x)
                if v_next == delivery_pos:
                    agent.task.status = Task.STATUS_COMPLETED
                    agent.task = None
            elif agent.target_task is not None:
                # Free agent reached pickup location
                pickup_pos = (agent.target_task.y, agent.target_task.x)
                if v_next == pickup_pos and agent.target_task.status == Task.STATUS_PENDING:
                    self._assign_task(agent, agent.target_task)

        return positions

    def is_complete(self) -> bool:
        """Check if all tasks are completed."""
        return all(t.status == Task.STATUS_COMPLETED for t in self.tasks)

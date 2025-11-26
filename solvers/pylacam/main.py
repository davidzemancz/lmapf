# define problem instance
from lacam import LaCAM
from mapf_utils import get_grid, get_scenario, validate_mapf_solution

map_file = "./solvers/lacam/assets/tunnel.map"
map_file = "./solvers/lacam/assets/random-32-32-10.map"
scen_file = "./solvers/lacam/assets/tunnel.scen"
scen_file = "./solvers/lacam/assets/random-32-32-10-random-1.scen"
num_agents = 100


grid = get_grid(map_file)
starts, goals = get_scenario(scen_file, num_agents)

# solve MAPF
planner = LaCAM()
solution = planner.solve(
    grid=grid,
    starts=starts,
    goals=goals,
    seed=0,
    time_limit_ms=10_000,
    flg_star=True,
    verbose=1,
)
validate_mapf_solution(grid, starts, goals, solution)
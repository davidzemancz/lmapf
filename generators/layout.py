from models.layout import Layout


def storage_floor(width: int, height: int) -> Layout:
    layout = Layout(width, height)

    # Storage everywhere
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            layout.set_value(x, y, Layout.CELL_STORAGE)

    # Output at (0, 0)
    layout.set_value(0, 0, Layout.CELL_OUTPUT)

    layout.compute_storage_cells()
    layout.compute_output_cells()

    return layout

def storage_walls(width: int, height: int) -> Layout:
    layout = Layout(width, height)

    # Create shelf blocks of 4x2 with spaces around them
    # Pattern: shelf block (4 wide x 2 tall) + 1 space horizontally, 1 space vertically
    block_width = 4
    block_height = 2
    spacing_x = 1  # Horizontal spacing between blocks
    spacing_y = 1  # Vertical spacing between blocks
    border_space = 2  # Space between shelves and borders
    
    # Calculate pattern repeat (block + spacing)
    pattern_width = block_width + spacing_x
    pattern_height = block_height + spacing_y
    
    # Leave 2 cells border space
    for y in range(border_space, height - border_space):
        for x in range(border_space, width - border_space):
            # Calculate position within pattern
            pattern_x = (x - border_space) % pattern_width
            pattern_y = (y - border_space) % pattern_height
            
            # If within shelf block dimensions (not in spacing), place storage
            if pattern_x < block_width and pattern_y < block_height:
                layout.set_value(x, y, Layout.CELL_STORAGE)
    
    # Add outputs on the borders (top and bottom)
    for x in range(width):
        if x % 2 == 0:
            layout.set_value(x, 0, Layout.CELL_OUTPUT)
            layout.set_value(x, height - 1, Layout.CELL_OUTPUT)

    layout.compute_storage_cells()
    layout.compute_output_cells()

    return layout

def obstacle_walls(width: int, height: int) -> Layout:
    layout = Layout(width, height)

    # Create obstacle blocks with storage around them
    # Pattern: obstacle block (4 wide x 2 tall) + 3 cells spacing between blocks
    block_width = 4
    block_height = 2
    spacing_x = 3  # 3 cells horizontal spacing between obstacle blocks
    spacing_y = 3  # 3 cells vertical spacing between obstacle blocks
    border_space = 2  # Space between obstacles and borders
    
    # Calculate pattern repeat (block + spacing)
    pattern_width = block_width + spacing_x
    pattern_height = block_height + spacing_y
    
    # Track obstacle positions
    obstacle_positions = set()
    
    # Place obstacles in a grid pattern
    for y in range(border_space, height - border_space):
        for x in range(border_space, width - border_space):
            # Calculate position within pattern
            pattern_x = (x - border_space) % pattern_width
            pattern_y = (y - border_space) % pattern_height
            
            # If within obstacle block dimensions (not in spacing), place obstacle
            if pattern_x < block_width and pattern_y < block_height:
                layout.set_value(x, y, Layout.CELL_OBSTACLE)
                obstacle_positions.add((x, y))
    
    # Place storage around obstacles (adjacent to obstacle blocks)
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            current_value = layout.get_value(x, y)
            # If cell is empty, check if it's adjacent to an obstacle
            if current_value == Layout.CELL_EMPTY:
                # Check 4 directions for adjacent obstacles
                adjacent_to_obstacle = False
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in obstacle_positions:
                        adjacent_to_obstacle = True
                        break
                
                if adjacent_to_obstacle:
                    layout.set_value(x, y, Layout.CELL_STORAGE)
    
    # Add outputs on the borders (top and bottom)
    for x in range(width):
        if x % 2 == 0:
            layout.set_value(x, 0, Layout.CELL_OUTPUT)
            layout.set_value(x, height - 1, Layout.CELL_OUTPUT)

    layout.compute_storage_cells()
    layout.compute_output_cells()

    return layout
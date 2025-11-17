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

    return layout
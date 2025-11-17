from models.layout import Layout

def floor_boxes(width: int, height: int) -> Layout:
    layout = Layout(width, height)

    # Storage everywhere
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            layout.set_value(x, y, Layout.CELL_FLOORBOX)

    # Output cells on the borders
    for x in range(width):
        if x % 2 == 0: 
            layout.set_value(x, 0, Layout.CELL_OUTPUT)
            layout.set_value(x, height - 1, Layout.CELL_OUTPUT)

    return layout
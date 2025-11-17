from models.layout import Layout

def read_from_file(file_path: str) -> Layout:
    with open(file_path, 'r') as f:
        first_line = f.readline().strip()
        width, height = map(int, first_line.split())
        layout = Layout(width, height)
        lines = f.readlines()
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                layout.grid[y][x] = int(char)

    raise ValueError("Layout dimensions not specified in file.")
                    
def save_to_file(layout: Layout, file_path: str):
    with open(file_path, 'w') as f:
        f.write(f"{layout.width} {layout.height}\n")
        for row in layout.grid:
            line = ''.join(str(cell) for cell in row)
            f.write(line + '\n')
from collections import deque

WALL = '#'
START = 'S'
GOAL = 'G'
PATH = 'P'

DIRECTION_MAP = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}

#This function scans the grid to find the coordinates of the specified character (either S or G). It returns a tuple of (row, column) if found, or None if not found.
def find_char(grid, ch):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ch:
                return (r, c)
    return None

# This function checks if the given coordinates (r, c) are within the bounds of the grid. It returns True if they are valid, and False otherwise.
def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


# This generator function yields valid neighboring coordinates in the order specified by move_order. It checks for walls and bounds before yielding neighbors.
def neighbors_in_order(grid, r, c, move_order):
    for direction in move_order:
        dr, dc = DIRECTION_MAP[direction]
        nr, nc = r + dr, c + dc

        if in_bounds(grid, nr, nc) and grid[nr][nc] != WALL:
            yield (nr, nc)


# This function implements BFS to find the shortest path from S to G while also counting the number of nodes expanded. It takes a move order to determine the order of neighbor exploration, which can lead to different paths being found.
def bfs_shortest_path_with_metrics(grid, move_order):
    start = find_char(grid, START)
    goal = find_char(grid, GOAL)

    if start is None or goal is None:
        raise ValueError("Grid must contain both S and G.")

    q = deque([start])
    visited = {start}
    parent = {start: None}

    nodes_expanded = 0

    while q:
        cur = q.popleft()
        nodes_expanded += 1

        if cur == goal:
            break

        for nxt in neighbors_in_order(grid, cur[0], cur[1], move_order):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                q.append(nxt)

    if goal not in parent:
        return [], 0, nodes_expanded

    path = []
    cur = goal

    while cur is not None:
        path.append(cur)
        cur = parent[cur]

    path.reverse()
    return path, len(path) - 1, nodes_expanded

# This function takes the original grid and a path (list of coordinates) and returns a new grid with the path overlaid using the PATH character.
def overlay_path_only(grid, path):
    grid2 = [list(row) for row in grid]

    for r, c in path:
        if grid2[r][c] not in (START, GOAL):
            grid2[r][c] = PATH

    return ["".join(row) for row in grid2]

# This function takes the original grid and a set of blocked cell coordinates, and returns a new grid with those cells temporarily marked as WALL.
def apply_temporary_blocks(grid, blocked_cells):
    grid2 = [list(row) for row in grid]

    for r, c in blocked_cells:
        if grid2[r][c] not in (START, GOAL):
            grid2[r][c] = WALL

    return ["".join(row) for row in grid2]

#here is where the candidate routes are originally generated. It will run BFS multiple times with different move orders and temporary blocks to generate a variety of candidate routes.
def generate_candidate_routes(grid, max_routes=3):
    move_orders = [
        ["UP", "RIGHT", "DOWN", "LEFT"],
        ["DOWN", "RIGHT", "UP", "LEFT"],
        ["RIGHT", "DOWN", "LEFT", "UP"],
        ["LEFT", "DOWN", "RIGHT", "UP"],
    ]

    routes = []
    seen_paths = set()
    blocked_cells = set()

    route_attempt = 1

    while len(routes) < max_routes and route_attempt <= 10:
        order = move_orders[(route_attempt - 1) % len(move_orders)]

        modified_grid = apply_temporary_blocks(grid, blocked_cells)

        path, steps, expanded = bfs_shortest_path_with_metrics(modified_grid, order)

        if path:
            path_key = tuple(path)

            if path_key not in seen_paths:
                seen_paths.add(path_key)

                routes.append({
                    "route_id": len(routes) + 1,
                    "move_order": order,
                    "path": path,
                    "distance": steps,
                    "nodes_expanded": expanded,
                })

                # Block one middle cell from this path to force the next route to differ. that way we get more variety in the candidate routes.
                middle_index = len(path) // 2
                blocked_cells.add(path[middle_index])

        route_attempt += 1

    return routes

# prints the grid in a readable format. Each row of the grid is printed on a new line.
def print_grid(grid):
    for row in grid:
        print(row)

import pygame
import sys
from queue import PriorityQueue, Queue, LifoQueue

pygame.init()

# Handle CLI algorithm input
selected_algorithm = "astar"
if len(sys.argv) > 1:
    selected_algorithm = sys.argv[1]

# Constants
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Visualizer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (64, 224, 208)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self): return self.color == RED
    def is_open(self): return self.color == GREEN
    def is_barrier(self): return self.color == BLACK
    def is_start(self): return self.color == ORANGE
    def is_end(self): return self.color == TURQUOISE

    def reset(self): self.color = WHITE
    def make_start(self): self.color = ORANGE
    def make_closed(self): self.color = RED
    def make_open(self): self.color = GREEN
    def make_barrier(self): self.color = BLACK
    def make_end(self): self.color = TURQUOISE
    def make_path(self): self.color = PURPLE

    def draw(self, win): pygame.draw.rect(win, self.color, (self.y, self.x, self.width, self.width))

    def update_neighbors(self, grid, diagonal=False):
        self.neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if diagonal:
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < self.total_rows and 0 <= c < self.total_rows:
                neighbor = grid[r][c]
                if not neighbor.is_barrier():
                    self.neighbors.append(neighbor)

    def __lt__(self, other): return False
    def __eq__(self, other): return isinstance(other, Node) and self.row == other.row and self.col == other.col
    def __hash__(self): return hash((self.row, self.col))


def h(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    f_score = g_score.copy()
    g_score[start] = 0
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False


def dijkstra(draw, grid, start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    dist = {node: float("inf") for row in grid for node in row}
    dist[start] = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = open_set.get()[1]

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp = dist[current] + 1
            if temp < dist[neighbor]:
                came_from[neighbor] = current
                dist[neighbor] = temp
                open_set.put((temp, neighbor))
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def bfs(draw, grid, start, end):
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {start}

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = queue.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.put(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def dfs(draw, grid, start, end):
    stack = LifoQueue()
    stack.put(start)
    came_from = {}
    visited = {start}

    while not stack.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = stack.get()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.put(neighbor)
                neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([Node(i, j, gap, rows) for j in range(rows)])
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    diagonal = False

    if selected_algorithm == "dijkstra":
        algorithm = dijkstra
    elif selected_algorithm == "bfs":
        algorithm = bfs
    elif selected_algorithm == "dfs":
        algorithm = dfs
    else:
        algorithm = astar

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                try:
                    row, col = get_clicked_pos(pygame.mouse.get_pos(), ROWS, width)
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != start and node != end:
                        node.make_barrier()
                except IndexError:
                    pass

            elif pygame.mouse.get_pressed()[2]:
                try:
                    row, col = get_clicked_pos(pygame.mouse.get_pos(), ROWS, width)
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None
                except IndexError:
                    pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid, diagonal)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_d:
                    diagonal = not diagonal

    pygame.quit()
    sys.exit()


main(WIN, WIDTH)

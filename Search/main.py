"""
Maze Solver
Author: Aryan Agrawal
"""

action = ["L", "R", "U", "D"]
#number of states explored global var
bfsc =0
dfsc =0
greedybestfirstsearchc = 0
astarc =0
class Node:
    def __init__(self, state, action, parent):
        self.state = state
        self.action = action
        self.parent = parent

class Queue:
    def __init__(self):
        self.queue = []

    def push(self, node):
        self.queue.append(node)

    def remove(self):
        ele = self.queue[0]
        self.queue = self.queue[1:]
        return ele

    def is_empty(self):
        return len(self.queue) == 0

    def is_in(self, state):
        for node in self.queue:
            if node.state == state:
                return True
        return False

class Stack(Queue):
    def remove(self):
        ele = self.queue[-1]
        self.queue = self.queue[:-1]
        return ele

def get_maze():
    maze = []
    with open('maze.txt') as f:
        for line in f:
            maze.append(list(line.strip().split(" ")))
    return maze

def print_maze(maze):
    for row in maze:
        print(" ".join(row))
    print()

def get_start(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'S':
                return (i, j)

def get_goal(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'G':
                return (i, j)

def get_neighbours(maze, node):
    neighbours = []
    i, j = node.state
    # Check each direction
    if i > 0 and maze[i - 1][j] != '#':  # Up
        neighbours.append((i - 1, j))
    if i < len(maze) - 1 and maze[i + 1][j] != '#':  # Down
        neighbours.append((i + 1, j))
    if j > 0 and maze[i][j - 1] != '#':  # Left
        neighbours.append((i, j - 1))
    if j < len(maze[i]) - 1 and maze[i][j + 1] != '#':  # Right
        neighbours.append((i, j + 1))
    return neighbours

def getaction(n, neighbour):
    if n.state[0] == neighbour[0]:
        if n.state[1] > neighbour[1]:
            return 'L'
        else:
            return 'R'
    else:
        if n.state[0] > neighbour[0]:
            return 'U'
        else:
            return 'D'

def solvebfs(maze, start, goal):
    s = Queue()
    s.push(Node(start, None, None))
    visited = []
    actions = []
    while True:
        if s.is_empty():
            raise Exception('No path found')
        n = s.remove()
        global bfsc
        bfsc+=1
        if n.state in visited:
            continue
        visited.append(n.state)
        if n.state == goal:
            path = []
            while n.parent is not None:
                path.append(n.state)
                actions.append(n.action)
                n = n.parent
            path.append(n.state)
            return actions[::-1], path[::-1]
        for neighbour in get_neighbours(maze, n):
            if neighbour not in visited and not s.is_in(neighbour):
                s.push(Node(neighbour, getaction(n, neighbour), n))

def solvedfs(maze, start, goal):
    s = Stack()
    s.push(Node(start, None, None))
    visited = []
    actions = []
    while True:
        if s.is_empty():
            raise Exception('No path found')
        n = s.remove()
        global dfsc
        dfsc+=1
        if n.state in visited:
            continue
        visited.append(n.state)
        if n.state == goal:
            path = []
            while n.parent is not None:
                path.append(n.state)
                actions.append(n.action)
                n = n.parent
            path.append(n.state)
            return actions[::-1], path[::-1]
        for neighbour in get_neighbours(maze, n):
            if neighbour not in visited and not s.is_in(neighbour):
                s.push(Node(neighbour, getaction(n, neighbour), n))

def heuristics(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def solvegreedybestfirstsearch(maze,start,goal):
    #assigning the heuristic value to each cell using manhattan distance
    h = []
    for i in range(len(maze)):
        h.append([])
        for j in range(len(maze[i])):
            h[i].append(heuristics((i,j),goal))
    s = Queue()
    s.push(Node(start,None,None))
    visited = []
    actions = []
    while True:
        if s.is_empty():
            raise Exception('No path found')
        n = s.remove()
        global greedybestfirstsearchc
        greedybestfirstsearchc+=1
        if n.state in visited:
            continue
        visited.append(n.state)
        if n.state == goal:
            path = []
            while n.parent!=None:
                path.append(n.state)
                actions.append(n.action)
                n = n.parent
            path.append(n.state)
            return actions[::-1], path[::-1]
        for neighbour in get_neighbours(maze,n):
            if neighbour not in visited and not s.is_in(neighbour):
                s.push(Node(neighbour,getaction(n,neighbour),n))
                s.queue = sorted(s.queue,key = lambda x: h[x.state[0]][x.state[1]])

def solveastar(maze,start,goal):
    #also store number of states explored
    #have heuristic as well as how many steps taken to come here
    h = []
    for i in range(len(maze)):
        h.append([])
        for j in range(len(maze[i])):
            h[i].append(heuristics((i,j),goal))
    s = Queue()
    s.push(Node(start,None,None))
    visited = []
    actions = []
    g = []
    for i in range(len(maze)):
        g.append([])
        for j in range(len(maze[i])):
            g[i].append(1000000)
    g[start[0]][start[1]] = 0
    while True:
        if s.is_empty():
            raise Exception('No path found')
        n = s.remove()
        global astarc
        astarc+=1
        if n.state in visited:
            continue
        visited.append(n.state)
        if n.state == goal:
            path = []
            while n.parent!=None:
                path.append(n.state)
                actions.append(n.action)
                n = n.parent
            path.append(n.state)
            return actions[::-1], path[::-1]
        for neighbour in get_neighbours(maze,n):
            if neighbour not in visited and not s.is_in(neighbour):
                s.push(Node(neighbour,getaction(n,neighbour),n))
                g[neighbour[0]][neighbour[1]] = g[n.state[0]][n.state[1]] + 1
                s.queue = sorted(s.queue,key = lambda x: h[x.state[0]][x.state[1]] + g[x.state[0]][x.state[1]])

def imagegen(path, action, name):
    from PIL import Image, ImageDraw
    maze = get_maze()
    size = [len(maze), len(maze[0])]
    im = Image.new('RGB', (size[1] * 100, size[0] * 100), color='white')
    draw = ImageDraw.Draw(im)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '#':
                draw.rectangle([j * 100, i * 100, j * 100 + 100, i * 100 + 100], fill='grey')
            elif maze[i][j] == 'S':
                draw.rectangle([j * 100, i * 100, j * 100 + 100, i * 100 + 100], fill='blue')
            elif maze[i][j] == 'G':
                draw.rectangle([j * 100, i * 100, j * 100 + 100, i * 100 + 100], fill='red')
    for cell in path:
        draw.rectangle([cell[1] * 100 + 20, cell[0] * 100 + 20, cell[1] * 100 + 80, cell[0] * 100 + 80], fill='lightgreen')
    im.save(name + '.png')

# Main
m = get_maze()
print_maze(m)
start = get_start(m)
goal = get_goal(m)
print("Start:", start, "End:", goal)
size = [len(m), len(m[0])]
print("Size:", size)
actions, path = solvebfs(m, start, goal)
imagegen(path[1:-1], actions,"bfs")
actions, path = solvedfs(m, start, goal)
imagegen(path[1:-1], actions,"dfs")
actions, path = solvegreedybestfirstsearch(m, start, goal)
imagegen(path[1:-1], actions,"greedybestfirstsearch")
actions, path = solveastar(m, start, goal)
imagegen(path[1:-1], actions,"astar")
print("Number of states explored: \n BFS:", bfsc, "\n DFS:", dfsc, "\n Greedy Best First Search:", greedybestfirstsearchc, "\n A*:", astarc)

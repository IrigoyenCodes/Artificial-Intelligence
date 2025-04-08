from collections import deque, defaultdict
from queue import PriorityQueue

class Graph:
    def __init__(self):
        # Initialize an empty adjacency list to store the graph
        self.graph = defaultdict(list)
    
    def add_edge(self, source, destination, cost):
        # Add an edge to the graph with its cost
        self.graph[source].append((destination, cost))


def bfs(graph, start, goal):
    """
    Breadth-First Search implementation
    Explores nodes level by level
    """
    # Queue stores (node, path, cost)
    queue = deque([(start, [start], 0)])
    visited = set()
    
    while queue:
        node, path, cost = queue.popleft()
        
        if node == goal:
            return path, cost
            
        if node not in visited:
            visited.add(node)
            
            # Add all unvisited neighbors to the queue
            for neighbor, edge_cost in graph.graph[node]:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    new_cost = cost + edge_cost
                    queue.append((neighbor, new_path, new_cost))
    
    return None, None


def dfs(graph, start, goal):
    """
    Depth-First Search implementation
    Explores nodes in depth, backtracking when necessary
    """
    # Stack stores (node, path, cost)
    stack = [(start, [start], 0)]
    visited = set()
    
    while stack:
        node, path, cost = stack.pop()
        
        if node == goal:
            return path, cost
            
        if node not in visited:
            visited.add(node)
            
            # Add all unvisited neighbors to the stack
            for neighbor, edge_cost in graph.graph[node]:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    new_cost = cost + edge_cost
                    stack.append((neighbor, new_path, new_cost))
    
    return None, None


def ucs(graph, start, goal):
    """
    Uniform Cost Search implementation
    Explores nodes in order of accumulated cost
    """
    # Priority queue stores (cost, node, path)
    pq = PriorityQueue()
    pq.put((0, start, [start]))
    visited = set()
    
    while not pq.empty():
        cost, node, path = pq.get()
        
        if node == goal:
            return path, cost
            
        if node not in visited:
            visited.add(node)
            
            # Add all unvisited neighbors to the priority queue
            for neighbor, edge_cost in graph.graph[node]:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    new_cost = cost + edge_cost
                    pq.put((new_cost, neighbor, new_path))
    
    return None, None



def main():
    # Create and populate the graph
    g = Graph()
    
    edges = [
        ('A', 'B', 1),
        ('A', 'C', 4),
        ('B', 'D', 2),
        ('C', 'D', 1),
        ('D', 'E', 3)
    ]
    

    for source, dest, cost in edges:
        g.add_edge(source, dest, cost)
    
    # Test all three algorithms
    start_node = 'A'
    goal_node = 'E'
    
    # Run BFS
    bfs_path, bfs_cost = bfs(g, start_node, goal_node)
    print("\nBFS Results:")
    print(f"Path: {' -> '.join(bfs_path)}")
    print(f"Cost: {bfs_cost}")
    
    # Run DFS
    dfs_path, dfs_cost = dfs(g, start_node, goal_node)
    print("\nDFS Results:")
    print(f"Path: {' -> '.join(dfs_path)}")
    print(f"Cost: {dfs_cost}")
    
    # Run UCS
    ucs_path, ucs_cost = ucs(g, start_node, goal_node)
    print("\nUCS Results:")
    print(f"Path: {' -> '.join(ucs_path)}")
    print(f"Cost: {ucs_cost}")

if __name__ == "__main__":
    main()
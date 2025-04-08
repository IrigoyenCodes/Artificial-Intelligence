import heapq

class Graph:
    def __init__(self):
        self.edges = {}
        self.heuristics = {}
    
    def add_edge(self, from_node, to_node, cost):
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append((to_node, cost))
    
    def set_heuristic(self, node, value):
        self.heuristics[node] = value
    
    def a_star(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (self.heuristics[start], 0, start, []))  # (f, g, node, path)
        visited = {}
        
        while open_set:
            f, g, current, path = heapq.heappop(open_set)
            
            if current in visited and visited[current] <= g:
                continue
            
            path = path + [current]
            visited[current] = g
            
            if current == goal:
                return path, g
            
            for neighbor, cost in self.edges.get(current, []):
                new_g = g + cost
                new_f = new_g + self.heuristics[neighbor]
                heapq.heappush(open_set, (new_f, new_g, neighbor, path))
        
        return None, float('inf')


graph = Graph()

graph.add_edge("A", "B", 10)
graph.add_edge("A", "C", 15)
graph.add_edge("B", "D", 12)
graph.add_edge("C", "D", 10)
graph.add_edge("D", "E", 5)

graph.set_heuristic("A", 20)
graph.set_heuristic("B", 15)
graph.set_heuristic("C", 10)
graph.set_heuristic("D", 5)
graph.set_heuristic("E", 0)

start, goal = "A", "E"
path, cost = graph.a_star(start, goal)

print(f"Ruta óptima: {path}, Costo total: {cost}")

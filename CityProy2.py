from queue import PriorityQueue

class Graph:
    def __init__(self):
        self.graph = {}      # Store city connections and distances
        self.heuristic = {}  # Store straight-line distances to goal
    
    def add_edge(self, city1, city2, distance):
        # Add cities and their connections
        if city1 not in self.graph:
            self.graph[city1] = {}
        if city2 not in self.graph:
            self.graph[city2] = {}
        
        self.graph[city1][city2] = distance
        self.graph[city2][city1] = distance
    
    def add_heuristic(self, city, distance_to_goal):
        # Add straight-line distance to goal
        self.heuristic[city] = distance_to_goal

def astar(graph, start, goal):
    # Priority queue to store (f_score, city, path, cost)
    frontier = PriorityQueue()
    frontier.put((0, start, [start], 0))
    
    # Keep track of visited cities
    visited = set()
    
    while not frontier.empty():
        f_score, current, path, cost = frontier.get()
        
        # Check if we reached the goal
        if current == goal:
            return path, cost
        
        # Skip if already visited
        if current in visited:
            continue
            
        visited.add(current)
        
        # Check all neighboring cities
        for next_city, distance in graph.graph[current].items():
            if next_city not in visited:
                new_cost = cost + distance
                h_score = graph.heuristic[next_city]  # Estimated distance to goal
                f_score = new_cost + h_score         # Total estimated cost
                new_path = path + [next_city]
                
                frontier.put((f_score, next_city, new_path, new_cost))
    
    return None, None

# Example usage
def main():
    # Create graph
    g = Graph()
    
    # Add city connections (city1, city2, distance)
    cities = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "D", 3),
        ("C", "D", 1),
        ("D", "E", 5)
    ]
    
    # Add straight-line distances to goal 'E'
    heuristics = {
        "A": 7,
        "B": 5,
        "C": 4,
        "D": 3,
        "E": 0
    }
    
    # Build the graph
    for city1, city2, dist in cities:
        g.add_edge(city1, city2, dist)
    
    # Add heuristics
    for city, h_dist in heuristics.items():
        g.add_heuristic(city, h_dist)
    
    # Find path from A to E
    path, cost = astar(g, "A", "E")
    
    # Print results
    if path:
        print("Path found:", " -> ".join(path))
        print("Total cost:", cost)
    else:
        print("No path found!")

if __name__ == "__main__":
    main()
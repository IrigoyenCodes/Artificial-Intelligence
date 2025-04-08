from typing import Dict, List, Set, Tuple
import heapq
from math import sqrt

class CityNetwork:
    def __init__(self):
        # Initialize the graph as an adjacency list and city positions
        self.graph: Dict[str, Dict[str, int]] = {}
        # Store (x, y) coordinates for each city for heuristic calculation
        self.positions: Dict[str, Tuple[float, float]] = {
            'A': (0, 0), 'B': (1, 1), 'C': (0, 2),
            'D': (2, 2), 'E': (2, 0), 'F': (1, 3),
            'G': (0, 4), 'H': (3, 1), 'I': (2, 4),
            'J': (1, 5)
        }
        
    def add_road(self, city1: str, city2: str, cost: int):
        """Add a bidirectional road between two cities."""
        if city1 not in self.graph:
            self.graph[city1] = {}
        if city2 not in self.graph:
            self.graph[city2] = {}
        
        self.graph[city1][city2] = cost
        self.graph[city2][city1] = cost
    
    def heuristic(self, city: str, goal: str) -> float:
        """
        Calculate the heuristic value (estimated cost) from city to goal.
        Uses Euclidean distance scaled by a factor to make it admissible.
        """
        x1, y1 = self.positions[city]
        x2, y2 = self.positions[goal]
        # Euclidean distance divided by 2 to ensure it's admissible
        # (never overestimates the true cost)
        return sqrt((x2 - x1)**2 + (y2 - y1)**2) / 2
        
    def a_star_search(self, start: str, goal: str) -> Tuple[List[str], int]:
        """
        Implement A* Search to find the optimal path.
        Returns: (path, total_cost)
        """
        # Priority queue entries are (f_score, g_score, current_city, path)
        # f_score = g_score + heuristic
        # g_score = cost from start to current_city
        pq = [(self.heuristic(start, goal), 0, start, [start])]
        # Keep track of visited cities and their lowest g_scores
        g_scores = {start: 0}
        
        while pq:
            f_score, g_score, current_city, path = heapq.heappop(pq)
            
            # If we reached the goal, return the path and cost
            if current_city == goal:
                return path, g_score
            
            # If we've already found a better path to this city, skip
            if current_city in g_scores and g_scores[current_city] < g_score:
                continue
                
            # Explore neighbors
            for neighbor, cost in self.graph[current_city].items():
                new_g_score = g_score + cost
                
                if neighbor not in g_scores or new_g_score < g_scores[neighbor]:
                    g_scores[neighbor] = new_g_score
                    new_path = path + [neighbor]
                    f_score = new_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(pq, (f_score, new_g_score, neighbor, new_path))
        
        return [], 0  # No path found

def create_network() -> CityNetwork:
    """Create the network from the example."""
    network = CityNetwork()
    
    # Add roads with their costs
    roads = [
        ("A", "B", 1), ("A", "C", 4),
        ("B", "D", 5), ("B", "E", 2),
        ("C", "F", 3), ("C", "G", 4),
        ("D", "H", 3), ("E", "H", 6),
        ("F", "I", 4), ("G", "J", 2),
        ("H", "I", 1), ("I", "J", 2)
    ]
    
    for city1, city2, cost in roads:
        network.add_road(city1, city2, cost)
    
    return network

def main():
    # Create the network
    network = create_network()
    
    # Find the optimal path from A to J using A*
    start_city = "A"
    goal_city = "J"
    path, total_cost = network.a_star_search(start_city, goal_city)
    
    if path:
        print("\nA* Search Results:")
        print("-" * 30)
        print(f"Path found: {' -> '.join(path)}")
        print(f"Total cost: {total_cost}")
        
        # Print detailed segment costs
        print("\nDetailed path segments:")
        print("-" * 30)
        for i in range(len(path)-1):
            current = path[i]
            next_city = path[i+1]
            segment_cost = network.graph[current][next_city]
            print(f"{current} to {next_city}: Cost = {segment_cost}")
    else:
        print("No path found!")

if __name__ == "__main__":
    main()
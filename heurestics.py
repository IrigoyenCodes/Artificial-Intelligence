from typing import Dict, List, Set, Tuple
import heapq

class CityNetwork:
    def __init__(self):
        # Initialize the graph as an adjacency list
        self.graph: Dict[str, Dict[str, int]] = {}
        # Store heuristic values
        self.heuristics: Dict[str, int] = {}

    def add_road(self, city1: str, city2: str, cost: int):
        """Add a bidirectional road between two cities."""
        if city1 not in self.graph:
            self.graph[city1] = {}
        if city2 not in self.graph:
            self.graph[city2] = {}
        
        self.graph[city1][city2] = cost
        self.graph[city2][city1] = cost

    def add_heuristic(self, city: str, value: int):
        """Add heuristic value for a city."""
        self.heuristics[city] = value

    def a_star_search(self, start: str, goal: str) -> Tuple[List[str], int]:
        """
        Implement A* search algorithm to find the optimal path.
        Returns: (path, total_cost)
        """
        # Priority queue of (f_score, current_cost, path)
        pq = [(self.heuristics[start], 0, [start])]
        visited = set()

        while pq:
            _, current_cost, path = heapq.heappop(pq)
            current = path[-1]

            if current == goal:
                return path, current_cost

            if current in visited:
                continue

            visited.add(current)

            for neighbor, cost in self.graph[current].items():
                if neighbor not in visited:
                    new_cost = current_cost + cost
                    new_path = path + [neighbor]
                    f_score = new_cost + self.heuristics[neighbor]
                    heapq.heappush(pq, (f_score, new_cost, new_path))

        return [], 0  # No path found

def create_example_network() -> CityNetwork:
    """Create the network from the example."""
    network = CityNetwork()
    
    # Add roads
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
    
    # Add heuristic values
    heuristics = {
        "A": 7, "B": 6, "C": 3,
        "D": 5, "E": 4, "F": 2,
        "G": 1, "H": 3, "I": 1,
        "J": 0  # destination
    }
    
    for city, value in heuristics.items():
        network.add_heuristic(city, value)
    
    return network

def main():
    # Create the network
    network = create_example_network()
    
    # Find optimal path from A to J
    path, total_cost = network.a_star_search("A", "J")
    
    if path:
        print("Optimal Route Found:")
        print(" -> ".join(path))
        print(f"Total Cost: {total_cost}")
        
        # Print detailed path information
        print("\nDetailed Path:")
        for i in range(len(path)-1):
            current = path[i]
            next_city = path[i+1]
            cost = network.graph[current][next_city]
            print(f"{current} to {next_city}: Cost = {cost}")
    else:
        print("No path found!")

if __name__ == "__main__":
    main()
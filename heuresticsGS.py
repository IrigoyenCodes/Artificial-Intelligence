from typing import Dict, List, Set, Tuple
import heapq

class CityNetwork:
    def __init__(self):
        # Initialize the graph as an adjacency list
        self.graph: Dict[str, Dict[str, int]] = {}
        
    def add_road(self, city1: str, city2: str, cost: int):
        """Add a bidirectional road between two cities."""
        if city1 not in self.graph:
            self.graph[city1] = {}
        if city2 not in self.graph:
            self.graph[city2] = {}
        
        self.graph[city1][city2] = cost
        self.graph[city2][city1] = cost
        
    def greedy_search(self, start: str, goal: str) -> Tuple[List[str], int]:
        """
        Implement Greedy Search to find a path based on lowest immediate cost.
        Returns: (path, total_cost)
        """
        # If start or goal not in graph, return empty path
        if start not in self.graph or goal not in self.graph:
            return [], 0
            
        current_city = start
        path = [start]
        total_cost = 0
        visited = {start}
        
        while current_city != goal:
            # Find unvisited neighbor with lowest direct cost
            neighbors = self.graph[current_city].items()
            best_cost = float('inf')
            best_neighbor = None
            
            for neighbor, cost in neighbors:
                if neighbor not in visited and cost < best_cost:
                    best_cost = cost
                    best_neighbor = neighbor
            
            # If no unvisited neighbors, we're stuck
            if best_neighbor is None:
                return [], 0
                
            # Move to the best neighbor
            current_city = best_neighbor
            path.append(current_city)
            total_cost += best_cost
            visited.add(current_city)
            
            # If we reached the goal, return the path and cost
            if current_city == goal:
                return path, total_cost
                
        return path, total_cost

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
    
    # Find a path from A to J using greedy search
    start_city = "A"
    goal_city = "J"
    path, total_cost = network.greedy_search(start_city, goal_city)
    
    if path:
        print("\nGreedy Search Results:")
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
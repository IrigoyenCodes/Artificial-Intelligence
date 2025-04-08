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

    def uniform_cost_search(self, start: str, goal: str) -> Tuple[List[str], int]:
        """
        Implement Uniform Cost Search to find the lowest-cost path.
        Returns: (path, total_cost)
        """
        # Priority queue entries are (cumulative_cost, current_city, path)
        pq = [(0, start, [start])]
        # Keep track of visited cities and their lowest costs
        visited = {}

        while pq:
            current_cost, current_city, path = heapq.heappop(pq)
            
            # If we reached the goal, return the path and cost
            if current_city == goal:
                return path, current_cost
            
            # If we've already found a better path to this city, skip
            if current_city in visited and visited[current_city] < current_cost:
                continue
                
            # Mark this city as visited with its cost
            visited[current_city] = current_cost
            
            # Explore neighbors
            for neighbor, cost in self.graph[current_city].items():
                if neighbor not in visited or visited[neighbor] > current_cost + cost:
                    new_cost = current_cost + cost
                    new_path = path + [neighbor]
                    heapq.heappush(pq, (new_cost, neighbor, new_path))

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
    
    # Find the optimal path from A to J using UCS
    start_city = "A"
    goal_city = "J"
    path, total_cost = network.uniform_cost_search(start_city, goal_city)
    
    if path:
        print("\nUniform Cost Search Results:")
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
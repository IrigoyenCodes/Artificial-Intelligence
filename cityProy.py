from queue import PriorityQueue
from typing import Dict, List, Set, Tuple
import heapq

class CityGraph:
    def __init__(self):
        # Initialize graph and heuristics as dictionaries
        self.graph = {}  # adjacency list with costs
        self.heuristics = {}  # straight-line distances to target
    
    def add_edge(self, city1: str, city2: str, distance: float):
        """Add a bidirectional edge between cities with given distance"""
        if city1 not in self.graph:
            self.graph[city1] = {}
        if city2 not in self.graph:
            self.graph[city2] = {}
        
        # Add bidirectional edges
        self.graph[city1][city2] = distance
        self.graph[city2][city1] = distance
    
    def add_heuristic(self, city: str, target: str, distance: float):
        """Add heuristic value (straight-line distance) from city to target"""
        if city not in self.heuristics:
            self.heuristics[city] = {}
        self.heuristics[city][target] = distance

def astar(graph: CityGraph, start: str, target: str) -> Tuple[List[str], float]:
    """
    A* algorithm implementation for finding the shortest path between cities
    
    Args:
        graph: CityGraph object containing the map and heuristics
        start: Starting city name
        target: Target city name
    
    Returns:
        Tuple containing:
            - List of cities representing the optimal path
            - Total cost of the path
    """
    # Priority queue entries are: (f_score, current_cost, city, path)
    pq = [(0, 0, start, [start])]
    visited = set()
    
    while pq:
        f_score, current_cost, current_city, path = heapq.heappop(pq)
        
        # If we've reached the target, return the path and cost
        if current_city == target:
            return path, current_cost
        
        # Skip if we've already visited this city
        if current_city in visited:
            continue
        
        visited.add(current_city)
        
        # Explore all neighboring cities
        for next_city, distance in graph.graph[current_city].items():
            if next_city not in visited:
                # Calculate costs
                g_score = current_cost + distance  # cost from start to next_city
                h_score = graph.heuristics[next_city].get(target, float('inf'))  # heuristic to target
                f_score = g_score + h_score  # total estimated cost
                
                # Create new path including this city
                new_path = path + [next_city]
                
                # Add to priority queue
                heapq.heappush(pq, (f_score, g_score, next_city, new_path))
    
    # If no path is found, return None
    return None, None

def main():
    # Create a new graph
    city_map = CityGraph()
    
    # Example city connections (you can modify these or read from a file)
    connections = [
        ("New York", "Boston", 215),
        ("New York", "Philadelphia", 97),
        ("Boston", "Philadelphia", 308),
        ("Philadelphia", "Washington", 139),
        ("Washington", "Richmond", 109),
    ]
    
    # Example heuristic distances to Richmond (target)
    heuristics = [
        ("New York", "Richmond", 354),
        ("Boston", "Richmond", 550),
        ("Philadelphia", "Richmond", 250),
        ("Washington", "Richmond", 109),
        ("Richmond", "Richmond", 0),
    ]
    
    # Build the graph
    for city1, city2, distance in connections:
        city_map.add_edge(city1, city2, distance)
    
    # Add heuristics
    for city, target, distance in heuristics:
        city_map.add_heuristic(city, target, distance)
    
    # Find path from New York to Richmond
    start_city = "New York"
    target_city = "Richmond"
    
    path, total_cost = astar(city_map, start_city, target_city)
    
    if path:
        print("\nA* Search Results:")
        print(f"Optimal Path: {' -> '.join(path)}")
        print(f"Total Distance: {total_cost} km")
    else:
        print(f"\nNo path found from {start_city} to {target_city}")

if __name__ == "__main__":
    main()
from collections import deque
from typing import List, Tuple, Set, Optional

class TreasureHunt:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def is_valid_move(self, x: int, y: int) -> bool:
        return (0 <= x < self.rows and 
                0 <= y < self.cols and 
                self.grid[x][y] != 1)

    def find_treasure_bfs(self, start_x: int, start_y: int, 
                         treasure_x: int, treasure_y: int) -> Optional[List[Tuple[int, int]]]:
        if not self.is_valid_move(start_x, start_y):
            return None

        queue = deque([(start_x, start_y)])
        visited = {(start_x, start_y)}
        parent = {(start_x, start_y): None}
        
        while queue:
            current_x, current_y = queue.popleft()
            
            if (current_x, current_y) == (treasure_x, treasure_y):
                return self._reconstruct_path(parent, (treasure_x, treasure_y))
            
            for dx, dy in self.directions:
                next_x, next_y = current_x + dx, current_y + dy
                
                if (self.is_valid_move(next_x, next_y) and 
                    (next_x, next_y) not in visited):
                    queue.append((next_x, next_y))
                    visited.add((next_x, next_y))
                    parent[(next_x, next_y)] = (current_x, current_y)
        
        return None

    def find_treasure_dfs(self, start_x: int, start_y: int,
                         treasure_x: int, treasure_y: int) -> Optional[List[Tuple[int, int]]]:
        visited = set()
        final_path = []
        
        def dfs(x: int, y: int) -> bool:
            if not self.is_valid_move(x, y) or (x, y) in visited:
                return False
            
            visited.add((x, y))
            final_path.append((x, y))
            
            if (x, y) == (treasure_x, treasure_y):
                return True
            
            for dx, dy in self.directions:
                next_x, next_y = x + dx, y + dy
                if dfs(next_x, next_y):
                    return True
            
            final_path.pop()
            return False
        
        return final_path if dfs(start_x, start_y) else None

    def _reconstruct_path(self, parent: dict, 
                         end: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent[current]
        return list(reversed(path))

    def print_grid(self, title: str = "Initial Grid"):
        """Print the grid without any path."""
        print(f"\n{title}")
        print("+" + "-" * (self.cols * 4 - 1) + "+")
        for row in self.grid:
            print("|", end=" ")
            for cell in row:
                if cell == 1:
                    print("1", end=" | ")
                else:
                    print("0", end=" | ")
            print("\n+" + "-" * (self.cols * 4 - 1) + "+")

    def print_path(self, path: List[Tuple[int, int]], title: str = "") -> None:
        """Print the grid with a path."""
        if not path:
            print("\nNo valid path found to the treasure!")
            return

        visual_grid = [row[:] for row in self.grid]
        
        # Mark the path with '*'
        for x, y in path:
            if visual_grid[x][y] != 'T':
                visual_grid[x][y] = '*'
        
        if title:
            print(f"\n{title}")
        
        print("+" + "-" * (self.cols * 4 - 1) + "+")
        for row in visual_grid:
            print("|", end=" ")
            for cell in row:
                if cell == 1:
                    print("1", end=" | ")
                elif cell == '*':
                    print("*", end=" | ")
                else:
                    print("0", end=" | ")
            print("\n+" + "-" * (self.cols * 4 - 1) + "+")

def main():
    grid = [
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [1, 1, 0, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0]
    ]
    
    start_x, start_y = 0, 0
    treasure_x, treasure_y = 9, 9
    
    hunt = TreasureHunt(grid)
    
    # Print initial grid
    hunt.print_grid("Initial Grid (1: obstacle)")
    
    # Find and print BFS path
    bfs_path = hunt.find_treasure_bfs(start_x, start_y, treasure_x, treasure_y)
    if bfs_path:
        hunt.print_path(bfs_path, "BFS Path (1: obstacle, *: path)")
        print(f"BFS Path Length: {len(bfs_path)} steps")
    
    # Find and print DFS path
    dfs_path = hunt.find_treasure_dfs(start_x, start_y, treasure_x, treasure_y)
    if dfs_path:
        hunt.print_path(dfs_path, "DFS Path (1: obstacle, *: path)")
        print(f"DFS Path Length: {len(dfs_path)} steps")

if __name__ == "__main__":
    main()
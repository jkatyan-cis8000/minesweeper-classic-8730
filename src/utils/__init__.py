from typing import List, Tuple


def get_neighbors(row: int, col: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    """Get valid neighbor coordinates for a cell."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors


def count_mines_in_neighbors(neighbors: List[Tuple[int, int]], mine_positions: List[Tuple[int, int]]) -> int:
    """Count mines among the given neighbor positions."""
    mine_set = set(mine_positions)
    count = 0
    for nr, nc in neighbors:
        if (nr, nc) in mine_set:
            count += 1
    return count

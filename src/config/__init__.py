from typing import List

from src.types import Cell, CellState, Difficulty, Board


DIFFICULTY_CONFIGS = {
    Difficulty.BEGINNER: {"rows": 9, "cols": 9, "mine_count": 10},
    Difficulty.INTERMEDIATE: {"rows": 16, "cols": 16, "mine_count": 40},
    Difficulty.EXPERT: {"rows": 16, "cols": 30, "mine_count": 99},
}


def get_difficulty_config(difficulty: Difficulty) -> dict:
    """Get the configuration for a difficulty level."""
    return DIFFICULTY_CONFIGS[difficulty]


def create_board_from_difficulty(difficulty: Difficulty) -> Board:
    """Create an empty board based on difficulty."""
    config = DIFFICULTY_CONFIGS[difficulty]
    rows = config["rows"]
    cols = config["cols"]
    total_mines = config["mine_count"]

    grid: List[List[Cell]] = []
    for row in range(rows):
        grid_row: List[Cell] = []
        for col in range(cols):
            cell = Cell(
                row=row,
                col=col,
                is_mine=False,
                state=CellState.HIDDEN,
                adjacent_mines=0,
            )
            grid_row.append(cell)
        grid.append(grid_row)

    return Board(
        grid=grid,
        rows=rows,
        cols=cols,
        total_mines=total_mines,
    )

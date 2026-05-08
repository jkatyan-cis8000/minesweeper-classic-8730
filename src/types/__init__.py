from enum import Enum
from dataclasses import dataclass
from typing import List


class CellState(Enum):
    HIDDEN = "hidden"
    REVEALED = "revealed"
    FLAGGED = "flagged"


@dataclass
class Cell:
    row: int
    col: int
    is_mine: bool
    state: CellState
    adjacent_mines: int = 0


class Difficulty(Enum):
    BEGINNER = (9, 9, 10)
    INTERMEDIATE = (16, 16, 40)
    EXPERT = (16, 30, 99)

    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines


@dataclass
class Board:
    grid: List[List[Cell]]
    rows: int
    cols: int
    total_mines: int


@dataclass
class GameState:
    board: Board
    status: str
    first_move_made: bool

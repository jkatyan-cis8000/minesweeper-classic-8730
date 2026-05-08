# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- src/types/__init__.py: Core type definitions (Cell, CellState, Board, GameState, Difficulty)
- src/config/__init__.py: Difficulty level configurations (beginner, intermediate, expert)
- src/service/__init__.py: Game logic (initialize game, reveal cell, flag cell, check win/loss)
- src/service/__main__.py: Service entry point for testing
- src/ui/__init__.py: CLI interface (display board, parse user input, game loop)
- src/ui/__main__.py: CLI entry point

## Interfaces

### types
- `CellState` enum: HIDDEN, REVEALED, FLAGGED
- `Cell` dataclass: (row, col, is_mine, state, adjacent_mines)
- `Difficulty` enum: BEGINNER, INTERMEDIATE, EXPERT
- `Board` dataclass: grid (list[list[Cell]]), rows, cols, total_mines
- `GameState` dataclass: board, status (PLAYING, WON, LOST), first_move_made

### service
- `initialize_game(difficulty: Difficulty) -> GameState`: Create new game with random mines
- `reveal_cell(state: GameState, row: int, col: int) -> GameState`: Reveal cell, handle mine/empty
- `flag_cell(state: GameState, row: int, col: int) -> GameState`: Toggle flag on cell
- `check_win(state: GameState) -> bool`: Check if all non-mine cells revealed
- `check_loss(state: GameState) -> bool`: Check if any mine revealed

### ui
- `display_board(state: GameState, reveal_all: bool = False) -> str`: Render board to string
- `parse_input(input_str: str) -> tuple[str, int, int] | None`: Parse "r 1 2" or "f 3 4"
- `play_game(game_state: GameState) -> None`: Main game loop

## Shared Data Structures

### Cell
```
Cell:
  row: int
  col: int
  is_mine: bool
  state: CellState (HIDDEN, REVEALED, FLAGGED)
  adjacent_mines: int  # 0-8, only valid if not is_mine
```

### Board
```
Board:
  grid: List[List[Cell]]
  rows: int
  cols: int
  total_mines: int
```

### GameState
```
GameState:
  board: Board
  status: str (PLAYING, WON, LOST)
  first_move_made: bool
```

### Difficulty Config
```
Difficulty config includes:
  rows: int
  cols: int
  mine_count: int
```

## External Dependencies

No external dependencies required. Pure Python standard library.

import random
from ..types import GameState, Board, Cell, CellState, Difficulty
from ..utils import get_neighbors, count_mines_in_neighbors


def _get_neighbors(row: int, col: int, rows: int, cols: int) -> list[tuple[int, int]]:
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors


def _count_mines_in_neighbors(neighbors: list[tuple[int, int]], mine_positions: list[tuple[int, int]]) -> int:
    mine_set = set(mine_positions)
    count = 0
    for nr, nc in neighbors:
        if (nr, nc) in mine_set:
            count += 1
    return count


def initialize_game(difficulty: Difficulty) -> GameState:
    rows = difficulty.rows
    cols = difficulty.cols
    total_mines = difficulty.mines

    positions = [(r, c) for r in range(rows) for c in range(cols)]
    mine_positions = random.sample(positions, total_mines)
    mine_set = set(mine_positions)

    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            is_mine = (r, c) in mine_set
            adjacent = _count_mines_in_neighbors(_get_neighbors(r, c, rows, cols), mine_positions)
            cell = Cell(row=r, col=c, is_mine=is_mine, state=CellState.HIDDEN, adjacent_mines=adjacent)
            row.append(cell)
        grid.append(row)

    board = Board(grid=grid, rows=rows, cols=cols, total_mines=total_mines)
    return GameState(board=board, status="PLAYING", first_move_made=False)


def reveal_cell(state: GameState, row: int, col: int) -> GameState:
    if state.status in ("WON", "LOST"):
        return state

    cell = state.board.grid[row][col]
    if cell.state == CellState.REVEALED or cell.state == CellState.FLAGGED:
        return state

    if not state.first_move_made:
        state.first_move_made = True
        if cell.is_mine:
            return _place_mine_elsewhere(state, row, col)
    elif cell.is_mine:
        return _reveal_all_mines(state)

    if cell.is_mine:
        return _reveal_all_mines(state)

    new_grid = [r.copy() for r in state.board.grid]
    _reveal_recursive(new_grid, row, col)
    new_board = Board(
        grid=new_grid,
        rows=state.board.rows,
        cols=state.board.cols,
        total_mines=state.board.total_mines
    )
    return GameState(board=new_board, status="PLAYING", first_move_made=True)


def _place_mine_elsewhere(state: GameState, safe_row: int, safe_col: int) -> GameState:
    rows = state.board.rows
    cols = state.board.cols
    total_mines = state.board.total_mines

    positions = [(r, c) for r in range(rows) for c in range(cols) if (r, c) != (safe_row, safe_col)]
    mine_positions = random.sample(positions, total_mines)
    mine_set = set(mine_positions)

    grid = []
    for r in range(rows):
        new_row = []
        for c in range(cols):
            is_mine = (r, c) in mine_set
            if (r, c) == (safe_row, safe_col):
                adjacent = 0
            else:
                adjacent = _count_mines_in_neighbors(_get_neighbors(r, c, rows, cols), mine_positions)
            cell = Cell(row=r, col=c, is_mine=is_mine, state=CellState.HIDDEN, adjacent_mines=adjacent)
            new_row.append(cell)
        grid.append(new_row)

    board = Board(grid=grid, rows=rows, cols=cols, total_mines=total_mines)
    return GameState(board=new_board, status="PLAYING", first_move_made=True)


def _reveal_recursive(grid, row: int, col: int):
    rows = len(grid)
    cols = len(grid[0])
    cell = grid[row][col]

    if cell.state != CellState.HIDDEN:
        return

    cell.state = CellState.REVEALED

    if cell.adjacent_mines == 0 and not cell.is_mine:
        neighbors = _get_neighbors(row, col, rows, cols)
        for nr, nc in neighbors:
            if grid[nr][nc].state == CellState.HIDDEN:
                _reveal_recursive(grid, nr, nc)


def _reveal_all_mines(state: GameState) -> GameState:
    new_grid = []
    for r in range(state.board.rows):
        new_row = []
        for c in range(state.board.cols):
            cell = state.board.grid[r][c]
            if cell.is_mine:
                new_row.append(Cell(row=cell.row, col=cell.col, is_mine=True, state=CellState.REVEALED, adjacent_mines=cell.adjacent_mines))
            else:
                new_row.append(cell)
            new_grid.append(new_row)

    new_board = Board(
        grid=new_grid,
        rows=state.board.rows,
        cols=state.board.cols,
        total_mines=state.board.total_mines
    )
    return GameState(board=new_board, status="LOST", first_move_made=True)


def flag_cell(state: GameState, row: int, col: int) -> GameState:
    if state.status in ("WON", "LOST"):
        return state

    cell = state.board.grid[row][col]
    if cell.state == CellState.REVEALED:
        return state

    new_grid = [r.copy() for r in state.board.grid]
    new_grid[row][col] = Cell(
        row=cell.row,
        col=cell.col,
        is_mine=cell.is_mine,
        state=CellState.FLAGGED if cell.state != CellState.FLAGGED else CellState.HIDDEN,
        adjacent_mines=cell.adjacent_mines
    )
    new_board = Board(
        grid=new_grid,
        rows=state.board.rows,
        cols=state.board.cols,
        total_mines=state.board.total_mines
    )
    return GameState(board=new_board, status="PLAYING", first_move_made=state.first_move_made)


def check_win(state: GameState) -> bool:
    if state.status == "WON":
        return True

    revealed_count = 0
    total_cells = state.board.rows * state.board.cols
    total_mines = state.board.total_mines

    for r in range(state.board.rows):
        for c in range(state.board.cols):
            cell = state.board.grid[r][c]
            if cell.state == CellState.REVEALED:
                revealed_count += 1

    if revealed_count == total_cells - total_mines:
        return True

    return False


def check_loss(state: GameState) -> bool:
    if state.status == "LOST":
        return True

    for r in range(state.board.rows):
        for c in range(state.board.cols):
            cell = state.board.grid[r][c]
            if cell.is_mine and cell.state == CellState.REVEALED:
                return True

    return False

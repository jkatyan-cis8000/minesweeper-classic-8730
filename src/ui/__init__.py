from ..service import reveal_cell, flag_cell, check_win, check_loss
from ..types import CellState


def display_board(state, reveal_all=False):
    """Render the board to a string for display."""
    rows = state.board.rows
    cols = state.board.cols
    
    lines = []
    header = "   " + " ".join(f"{c:2d}" for c in range(cols))
    lines.append(header)
    lines.append("  +" + "---" * cols + "+")
    
    for r in range(rows):
        row_parts = [f"{r:2d}|"]
        for c in range(cols):
            cell = state.board.grid[r][c]
            if cell.state == CellState.HIDDEN and not reveal_all:
                row_parts.append(" ■ ")
            elif cell.state == CellState.FLAGGED:
                row_parts.append(" ▲ ")
            elif cell.state == CellState.REVEALED:
                if cell.is_mine:
                    row_parts.append(" * ")
                elif cell.adjacent_mines == 0:
                    row_parts.append("   ")
                else:
                    row_parts.append(f" {cell.adjacent_mines} ")
        row_parts.append("|")
        lines.append("".join(row_parts))
    
    lines.append("  +" + "---" * cols + "+")
    return "\n".join(lines)


def parse_input(input_str):
    """Parse user input in format 'r 1 2' or 'f 3 4'."""
    parts = input_str.strip().split()
    if len(parts) != 3:
        return None
    
    action, row_str, col_str = parts
    if action not in ("r", "f"):
        return None
    
    try:
        row = int(row_str)
        col = int(col_str)
        return (action, row, col)
    except ValueError:
        return None


def play_game(game_state):
    """Main game loop."""
    state = game_state
    
    print("Minesweeper Classic!")
    print("Commands: r <row> <col> to reveal, f <row> <col> to flag, q to quit")
    
    while state.status not in ("WON", "LOST"):
        print()
        print(display_board(state))
        print(f"Status: {state.status}")
        
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue
            
            if user_input.lower() == "q":
                print("Quitting...")
                return
            
            parsed = parse_input(user_input)
            if parsed is None:
                print("Invalid command. Use: r <row> <col>, f <row> <col>, q")
                continue
            
            action, row, col = parsed
            
            if row < 0 or row >= state.board.rows or col < 0 or col >= state.board.cols:
                print(f"Invalid position: ({row}, {col}). Board is {state.board.rows}x{state.board.cols}.")
                continue
            
            if action == "r":
                state = reveal_cell(state, row, col)
                if check_win(state):
                    state.status = "WON"
                elif check_loss(state):
                    state.status = "LOST"
            elif action == "f":
                state = flag_cell(state, row, col)
        
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
    
    print()
    print(display_board(state, reveal_all=True))
    
    if state.status == "WON":
        print("Congratulations! You won!")
    else:
        print("Game over! Better luck next time.")

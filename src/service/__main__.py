"""Service entry point for testing game logic."""

from ..config import Difficulty, DIFFICULTY_CONFIGS
from ..types import CellState
from ..service import initialize_game, reveal_cell, flag_cell, check_win, check_loss


def test_gameplay():
    """Test basic gameplay flow."""
    config = DIFFICULTY_CONFIGS[Difficulty.BEGINNER]
    state = initialize_game(Difficulty.BEGINNER)
    print(f"Game initialized: {state.board.rows}x{state.board.cols}, {state.board.total_mines} mines")
    
    revealed_count = 0
    total_cells = state.board.rows * state.board.cols
    total_mines = state.board.total_mines
    
    while state.status == "PLAYING" and revealed_count < total_cells - total_mines:
        for r in range(state.board.rows):
            for c in range(state.board.cols):
                if state.board.grid[r][c].state == CellState.HIDDEN:
                    state = reveal_cell(state, r, c)
                    if state.board.grid[r][c].state == CellState.REVEALED:
                        revealed_count += 1
                    break
        else:
            break
    
    if check_win(state):
        print("You won!")
    elif check_loss(state):
        print("Game over!")
    
    print(f"Final status: {state.status}")


def test_flagging():
    """Test flagging functionality."""
    state = initialize_game(Difficulty.BEGINNER)
    
    print("Testing flagging...")
    state = flag_cell(state, 0, 0)
    assert state.board.grid[0][0].state == CellState.FLAGGED
    print("Flag placed successfully")
    
    state = flag_cell(state, 0, 0)
    assert state.board.grid[0][0].state == CellState.HIDDEN
    print("Flag removed successfully")


def main():
    """Main entry point."""
    print("Running service tests...\n")
    
    try:
        test_gameplay()
        print()
        test_flagging()
        print("\nAll tests passed!")
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

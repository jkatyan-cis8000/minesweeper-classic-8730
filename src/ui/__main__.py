"""CLI entry point for Minesweeper Classic."""

from ..ui import play_game
from ..config import Difficulty, create_board_from_difficulty
from ..service import initialize_game
from ..types import GameState


def main():
    """Run the Minesweeper CLI."""
    import sys

    difficulty_name = "BEGINNER"

    if len(sys.argv) > 1:
        difficulty_name = sys.argv[1].upper()

    try:
        difficulty = getattr(Difficulty, difficulty_name)
    except AttributeError:
        print(f"Invalid difficulty: {difficulty_name}")
        print("Available: BEGINNER, INTERMEDIATE, EXPERT")
        sys.exit(1)

    game_state = initialize_game(difficulty)
    play_game(game_state)


if __name__ == "__main__":
    main()

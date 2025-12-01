from time import sleep

import PlacementGameCLI
import numpy as np
from typing import List, Any


def solve(game: PlacementGameCLI.PlacementGame, delay: int = 0):
    placements = calculate_placements(game)

    board_coverage = np.zeros((game.board_w, game.board_h))

    return search_step(game, placements, board_coverage, delay)


def search_step(game: PlacementGameCLI.PlacementGame, placements: List[Any], board_coverage: np.ndarray,
                delay: int = 0):
    # 1. Success check: board is full
    if game.check_win(): return True

    # 2. Choose an uncovered board cell (Algorithm X: choose column)
    cx, cy = None, None
    for x in range(game.board_w):
        for y in range(game.board_h):
            if not board_coverage[x][y]:
                cx, cy = x, y
                break
        if cx is not None:
            break

    # print_board_coverage(board_coverage, cx, cy, os.get_terminal_size().lines - game.board_h - len(game.pieces) - 10, delay)

    # 3. Collect placements that cover this cell (column)
    valid_placements = []
    for piece, x, y, rotate in placements:
        w = piece.w
        h = piece.h
        # Check if placement covers cell
        if x <= cx < x + w and y <= cy < y + h:
            valid_placements.append((piece, x, y, rotate))

    # No placements found - fail
    if not valid_placements:
        return False

    # 4. Try each candidate placement (starting with the least possible placements)
    valid_placements.sort(key=lambda p: p[3])

    for piece, x, y, rotate in valid_placements:
        if rotate: game.rotate(piece.id)
        game.place(piece.id, x, y)

        # Update board coverage
        board_coverage[x:x + piece.w, y:y + piece.h] = 1

        # Recursive search
        placements = calculate_placements(game)
        if search_step(game, placements, board_coverage, delay):
            return True

        # Revert placement
        game.remove(piece.id)
        board_coverage[x:x + piece.w, y:y + piece.h] = 0
        if rotate: game.rotate(piece.id)

    return False  # Failed to find solution


def print_board_coverage(board_coverage: np.ndarray[tuple[Any, ...], np.dtype[Any]], cx: int | None, cy: int | None,
                         height: int = 10, delay: int = 0):
    for j in range(board_coverage.shape[1])[:height]:
        row = ""
        for i in range(board_coverage.shape[0]):
            if j == cy and i == cx:
                row += f"\033[93m{int(board_coverage[i, j])}\033[0m "
            else:
                row += f"{int(board_coverage[i, j])} "
        print(row)
    # pause for delay
    if delay:
        sleep(delay)
    # input("Press Enter to continue...")


def calculate_placements(game: PlacementGameCLI.PlacementGame) -> list[Any]:
    placements = []

    for piece in game.pieces:
        if piece.placed: continue

        orientations = [(piece.w, piece.h, False)]
        if piece.w != piece.h:
            orientations.append((piece.h, piece.w, True))

        for w, h, rotate in orientations:
            for x in range(game.board_w - w + 1):
                for y in range(game.board_h - h + 1):
                    if not game.check_collision(piece, x, y, w, h):
                        placements.append((piece, x, y, rotate))

        piece.possible_placements = sum(1 for p, _, _, _ in placements if p == piece)
    return placements

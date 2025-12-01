import random
import os
import AlgorithmX as X

# --- LEVELS CONFIGURATION ---
LEVELS = [
    {
        "name": "Small",
        "width": 5,
        "height": 5,
        "pieces": [
            (3, 3, "#E74C3C"),
            (2, 3, "#3498DB"),
            (3, 2, "#2ECC71"),
            (2, 2, "#F1C40F"),
        ]
    },
    {
        "name": "Medium",
        "width": 8,
        "height": 8,
        "pieces": [
            (4, 4, "#E74C3C"),
            (4, 4, "#3498DB"),
            (4, 2, "#2ECC71"),
            (4, 2, "#F1C40F"),
            (2, 2, "#E67E22"),
            (2, 2, "#1ABC9C"),
            (2, 4, "#34495E"),
        ]
    },
    {
        "name": "Standard",
        "width": 11,
        "height": 10,
        "pieces": [
            (3, 2, "#E74C3C"),
            (3, 2, "#3498DB"),
            (6, 3, "#2ECC71"),
            (2, 4, "#F1C40F"),
            (3, 3, "#E67E22"),
            (4, 2, "#1ABC9C"),
            (3, 5, "#34495E"),
            (4, 3, "#8E44AD"),
            (1, 3, "#2980B9"),
            (4, 5, "#9B59B6"),
            (1, 5, "#95A5A6"),
        ]
    },
    {
        "name": "Big",
        "width": 20,
        "height": 20,
        "pieces": [
            (10, 10, "#E74C3C"),
            (8, 8, "#8E44AD"),
            (5, 8, "#3498DB"),
            (6, 6, "#1ABC9C"),
            (4, 9, "#2ECC71"),
            (5, 6, "#F1C40F"),
            (4, 6, "#E67E22"),
            (3, 7, "#D35400"),
            (3, 5, "#C0392B"),
            (2, 6, "#2980B9"),
            (2, 5, "#27AE60"),
            (2, 4, "#7F8C8D"),
            (2, 2, "#34495E")
        ]
    },
    {
        "name": "Insanity",
        "width": 40,
        "height": 20,
        "pieces": [
            (20, 9, "#C0392B"),
            (20, 7, "#E74C3C"),
            (10, 9, "#E67E22"),
            (10, 7, "#F39C12"),
            (10, 5, "#F1C40F"),
            (7, 5, "#27AE60"),
            (5, 5, "#16A085"),
            (6, 4, "#1ABC9C"),
            (4, 4, "#3498DB"),
            (5, 3, "#2980B9"),
            (3, 3, "#9B59B6"),
            (4, 2, "#8E44AD"),
            (2, 2, "#34495E"),
            (3, 2, "#2C3E50"),
            (1, 2, "#95A5A6"),
            (3, 1, "#7F8C8D"),
            (2, 1, "#C0392B"),
            (2, 1, "#E74C3C"),
            (1, 1, "#D35400"),
            (9, 5, "#E67E22"),
            (8, 4, "#F39C12"),
            (7, 4, "#F1C40F"),
            (6, 1, "#2ECC71"),
            (4, 1, "#16A085"),
            (3, 1, "#27AE60")
        ]
    }
]

def get_piece_volume_of_level(pieces):
    pieces = [
        (10, 10, "#E74C3C"),
        (8, 8, "#8E44AD"),
        (5, 8, "#3498DB"),
        (6, 6, "#1ABC9C"),
        (4, 9, "#2ECC71"),
        (5, 6, "#F1C40F"),
        (4, 6, "#E67E22"),
        (3, 7, "#D35400"),
        (3, 5, "#C0392B"),
        (2, 6, "#2980B9"),
        (2, 5, "#27AE60"),
        (2, 4, "#7F8C8D"),
        (2, 2, "#34495E")
    ]
    volume = 0
    for w, h, _ in pieces:
        volume += w * h
    return f"Total volume of pieces: {volume}"


def get_ansi_color(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    elif 'TERM' in os.environ:
        os.system('clear')
    else:
        print("\n" * 50)


class Piece:
    def __init__(self, pid, w, h, color):
        self.id = pid
        self.w = w
        self.h = h
        self.color = color
        self.x = -1
        self.y = -1
        self.placed = False
        self.possible_placements = -1


class PlacementGame:
    def __init__(self, level_config):
        self.print_enabled = True
        self.solve_delay = 0
        self.level_name = level_config["name"]
        self.board_w = level_config["width"]
        self.board_h = level_config["height"]
        self.initial_pieces_config = level_config["pieces"]

        self.pieces = []
        for i, (w, h, color) in enumerate(self.initial_pieces_config):
            self.pieces.append(Piece(i, w, h, color))

    def print(self):
        if not self.print_enabled:
            return
        clear_screen()
        print(f"Level: {self.level_name} ({self.board_w}x{self.board_h})")
        self.print_board()
        self.list_pieces()

    def print_board(self):
        grid = [[' .' for _ in range(self.board_w)] for _ in range(self.board_h)]
        for p in self.pieces:
            if p.placed:
                color_code = get_ansi_color(p.color)
                reset_code = "\033[0m"
                for r in range(p.y, p.y + p.h):
                    for c in range(p.x, p.x + p.w):
                        if 0 <= r < self.board_h and 0 <= c < self.board_w:
                            grid[r][c] = f"{color_code}{p.id:>2}{reset_code}"

        print("\n    " + " ".join(f"{i:>2}" for i in range(self.board_w)))
        for r in range(self.board_h):
            print(f"{r:>2}  " + " ".join(grid[r]))

    def list_pieces(self):
        print("\n--- Pieces ---")
        for p in self.pieces:
            color_code = get_ansi_color(p.color)
            reset_code = "\033[0m"
            state = f"Placed at ({p.x}, {p.y})" if p.placed else "Not placed"

            info = f"ID {p.id:>2}: {color_code}{p.w:>2}x{p.h:<2}{reset_code} | {state}"
            if not p.placed:
                if p.possible_placements >= 0:
                    info += f" | Possible placements: {p.possible_placements}"
            print(info)
        print("--------------\n")

    def check_collision(self, piece, x, y, w, h):
        if x < 0 or y < 0 or x + w > self.board_w or y + h > self.board_h:
            return True

        for p in self.pieces:
            if p.id != piece.id and p.placed:
                # Check overlap
                if not (x + w <= p.x or x >= p.x + p.w or
                        y + h <= p.y or y >= p.y + p.h):
                    return True
        return False

    def place(self, pid, x, y):
        if not (0 <= pid < len(self.pieces)):
            print(f"Error: Invalid piece ID {pid}")
            return

        p = self.pieces[pid]
        if self.check_collision(p, x, y, p.w, p.h):
            self.print()
            print(f"Error: Cannot place piece {pid} at ({x}, {y}). Collision or out of bounds.")
        else:
            p.x = x
            p.y = y
            p.placed = True
            self.print()
            print(f"Piece {pid} placed at ({x}, {y}).")
            self.check_win()

    def remove(self, pid):
        if not (0 <= pid < len(self.pieces)):
            print(f"Error: Invalid piece ID {pid}")
            return
        p = self.pieces[pid]
        if p.placed:
            p.placed = False
            p.x = -1
            p.y = -1
            self.print()
            print(f"Piece {pid} removed.")
        else:
            self.print()
            print(f"Piece {pid} is not placed.")

    def rotate(self, pid):
        if not (0 <= pid < len(self.pieces)):
            print(f"Error: Invalid piece ID {pid}")
            return

        p = self.pieces[pid]
        if p.placed:
            self.print()
            print(f"Piece {pid} is placed. Remove it first to rotate.")
            return

        p.w, p.h = p.h, p.w
        self.print()
        print(f"Piece {pid} rotated. New size: {p.w}x{p.h}")

    def check_win(self):
        if all(p.placed for p in self.pieces):
            total_area = sum(p.w * p.h for p in self.pieces)
            if total_area == self.board_w * self.board_h:
                print("\nCONGRATULATIONS! You have filled the board!\n")
                return True
            return False

    def reset(self):
        self.pieces = []
        for i, (w, h, color) in enumerate(self.initial_pieces_config):
            self.pieces.append(Piece(i, w, h, color))
        self.print()

    def shuffle(self):
        random.shuffle(self.pieces)
        self.print()

    def run(self):
        self.print()
        print(get_piece_volume_of_level(self.pieces))
        print("Placement Game CLI")
        print("Commands: place <id> <x> <y>, remove <id>, rotate <id>, shuffle, solve, quit")

        while True:
            try:
                line = input("> ").strip()
                if not line: continue
                parts = line.split()
                cmd = parts[0].lower()

                if cmd == "quit" or cmd == "exit":
                    break
                elif cmd == "reset":
                    self.reset()
                elif cmd == "list":
                    self.list_pieces()
                elif cmd == "show":
                    self.print_board()
                elif cmd == "solve":
                    X.solve(game, self.solve_delay)
                elif cmd == "rotate":
                    if len(parts) < 2:
                        print("Usage: rotate <id>")
                        continue
                    self.rotate(int(parts[1]))
                elif cmd == "remove":
                    if len(parts) < 2:
                        print("Usage: remove <id>")
                        continue
                    self.remove(int(parts[1]))
                elif cmd == "place":
                    if len(parts) < 4:
                        print("Usage: place <id> <x> <y>")
                        continue
                    self.place(int(parts[1]), int(parts[2]), int(parts[3]))
                elif cmd == "delay":
                    self.print()
                    if len(parts) < 2:
                        print(f"Current delay: {self.solve_delay}s. Usage: delay <seconds>")
                        continue
                    self.solve_delay = int(parts[1])
                    print(f"Delay set to {self.solve_delay}s")
                elif cmd == "print":
                    self.print_enabled = not self.print_enabled
                    print(f"Printing enabled: {self.print_enabled}")
                elif cmd == "shuffle":
                    self.shuffle()
                elif cmd == "help":
                    self.print()
                    print(
                        "Commands: place <id> <x> <y>, remove <id>, rotate <id>, delay <seconds>, shuffle, solve, reset, quit")
                else:
                    print("Unknown command")
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    while True:
        clear_screen()
        print("=== PLACEMENT GAME SELECTION ===")
        for i, level in enumerate(LEVELS):
            print(f"{i + 1}. {level['name']} ({level['width']}x{level['height']})")
        print("Q. Quit")

        choice = input("\nSelect Level: ").strip().lower()
        if choice == 'q':
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(LEVELS):
                game = PlacementGame(LEVELS[idx])
                game.run()
            else:
                input("Invalid selection! Press Enter...")
        except ValueError:
            input("Invalid selection! Press Enter...")

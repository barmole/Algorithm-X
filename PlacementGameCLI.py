import sys
import os
import time

# --- KONFIGURATION ---
BOARD_W = 11
BOARD_H = 10

# Die 10 Rechtecke (Breite, Höhe, Farbe)
RECTANGLES_CONFIG = [
    (3, 2, "#E74C3C"),  # Rot
    (3, 2, "#3498DB"),  # Blau
    (6, 3, "#2ECC71"),  # Grün
    (2, 4, "#F1C40F"),  # Gelb
    (3, 3, "#E67E22"),  # Orange
    (4, 2, "#1ABC9C"),  # Türkis
    (3, 5, "#34495E"),  # Dunkelgrau
    (4, 3, "#8E44AD"),  # Lila
    (4, 5, "#9B59B6"),  # Magenta
    (1, 5, "#95A5A6"),  # Grau
]

def get_ansi_color(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    elif 'TERM' in os.environ:
        os.system('clear')
    else:
        print("\n" * 50)

class AlgorithmX:
    def __init__(self, game):
        self.game = game
        self.steps = 0
        self.history = []

    def solve(self):
        self.steps = 0
        self.history = []

        print("Starting Algorithm X Search...")
        if self._search(set(range(len(self.game.pieces)))):
            print(f"\nSolution found in {self.steps} steps!")
        else:
            print(f"\nNo solution found after {self.steps} steps.")

    def render(self):
        clear_screen()
        self.game.print_board()
        self.game.list_pieces()
        print("\n--- History (Last 30 Steps) ---")
        for msg in self.history[-30:]:
            print(msg)
        print("--------------------------------------")
        time.sleep(self.game.solve_delay)

    def _search(self, remaining_piece_ids):
        # Base case: all pieces placed
        if not remaining_piece_ids:
            return True

        self.steps += 1

        # Determine occupied cells for collision checking
        occupied = set()
        for p in self.game.pieces:
            if p.placed:
                for r in range(p.y, p.y + p.h):
                    for c in range(p.x, p.x + p.w):
                        occupied.add((c, r))

        # Find the piece with the fewest valid moves (Algorithm X Heuristic)
        best_pid = -1
        min_moves = []
        min_count = float('inf')

        # Analyze all remaining pieces
        for pid in remaining_piece_ids:
            p = self.game.pieces[pid]
            self.game.pieces[pid].possible_placements = 0
            valid_moves = []

            # Try all orientations: (w, h) and (h, w) if different
            orientations = [(p.w, p.h)]
            if p.w != p.h:
                orientations.append((p.h, p.w))

            for w, h in orientations:
                # Try all board positions
                for y in range(BOARD_H - h + 1):
                    for x in range(BOARD_W - w + 1):
                        # Check collision
                        collision = False
                        for r in range(y, y + h):
                            if collision: break
                            for c in range(x, x + w):
                                if (c, r) in occupied:
                                    collision = True
                                    break
                        if not collision:
                            valid_moves.append((pid, x, y, w, h))
                            self.game.pieces[pid].possible_placements += 1

            # Update best candidate
            if len(valid_moves) < min_count:
                min_count = len(valid_moves)
                best_pid = pid
                min_moves = valid_moves
                # Optimization: fail fast if a piece has 0 moves
                if min_count == 0:
                    break
        
        # Log progress / Intermediate results
        indent = "  " * (len(self.game.pieces) - len(remaining_piece_ids))
        self.history.append(f"{indent}Step {self.steps}: Best candidate Piece {best_pid} has {min_count} moves")

        if min_count == 0:
            return False # Dead end

        # Try each move for the selected piece
        for move in min_moves:
            pid, x, y, w, h = move
            
            p = self.game.pieces[pid]
            original_w, original_h = p.w, p.h
            
            # Place piece
            p.x = x
            p.y = y
            p.w = w
            p.h = h
            p.placed = True
            
            self.history.append(f"{indent} -> Placing Piece {pid} at ({x}, {y})")
            self.render()
            
            # Recurse
            if self._search(remaining_piece_ids - {pid}):
                return True
            
            # Backtrack
            p.placed = False
            p.x = -1
            p.y = -1
            p.w = original_w
            p.h = original_h

            self.history.append(f"{indent} <- Backtracking Piece {pid}")
            self.render()
        
        return False

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
    def __init__(self):
        self.solve_delay = 1
        self.pieces = []
        for i, (w, h, color) in enumerate(RECTANGLES_CONFIG):
            self.pieces.append(Piece(i, w, h, color))

    def print(self):
        clear_screen()
        self.print_board()
        self.list_pieces()

    def print_board(self):
        grid = [[' .' for _ in range(BOARD_W)] for _ in range(BOARD_H)]
        for p in self.pieces:
            if p.placed:
                color_code = get_ansi_color(p.color)
                reset_code = "\033[0m"
                for r in range(p.y, p.y + p.h):
                    for c in range(p.x, p.x + p.w):
                        if 0 <= r < BOARD_H and 0 <= c < BOARD_W:
                            grid[r][c] = f"{color_code}{p.id:>2}{reset_code}"
    
        print("\n    " + " ".join(f"{i:>2}" for i in range(BOARD_W)))
        for r in range(BOARD_H):
            print(f"{r:>2}  " + " ".join(grid[r]))

    def list_pieces(self):
        print("\n--- Pieces ---")
        for p in self.pieces:
            color_code = get_ansi_color(p.color)
            reset_code = "\033[0m"
            state = f"Placed at ({p.x}, {p.y})" if p.placed else "Not placed"
            
            info = f"ID {p.id}: {color_code}{p.w}x{p.h}{reset_code} | {state}"
            if not p.placed:
                if p.possible_placements >= 0:
                    info += f" | Possible placements: {p.possible_placements}"
            print(info)
        print("--------------\n")

    def check_collision(self, piece, x, y, w, h):
        if x < 0 or y < 0 or x + w > BOARD_W or y + h > BOARD_H:
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
            if total_area == BOARD_W * BOARD_H:
                print("\nCONGRATULATIONS! You have filled the board!\n")

    def reset(self):
        # Reset back to Recktangle Config
        for p in self.pieces:
            p.w, p.h = RECTANGLES_CONFIG[p.id][0], RECTANGLES_CONFIG[p.id][1]
            p.x = -1
            p.y = -1
            p.placed = False
            p.possible_placements = -1
        self.print()

    def run(self):
        self.print()
        print("Placement Game CLI")
        print("Commands: place <id> <x> <y>, remove <id>, rotate <id>, solve, quit")
    
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
                    solver = AlgorithmX(self)
                    solver.solve()
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
                    self.solve_delay = float(parts[1])
                    print(f"Delay set to {self.solve_delay}s")
                elif cmd == "help":
                    self.print()
                    print("Commands: place <id> <x> <y>, remove <id>, rotate <id>, delay <seconds>, solve, reset, quit")
                else:
                    print("Unknown command")
            except ValueError:
                print("Invalid number format")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    game = PlacementGame()
    game.run()

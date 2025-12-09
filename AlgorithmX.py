from time import sleep, time

import PlacementGameCLI
import numpy as np
from typing import List, Any

class Node:
    def __init__(self, row_id=-1):
        self.left = self.right = self.up = self.down = self
        self.column = None
        self.row_id = row_id

class Column(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.size = 0

class DancingLinks:
    def __init__(self, matrix, col_names):
        self.head = Column("HEAD")
        self.solution = []

        # Spalten erstellen
        self.columns = []
        last = self.head
        for name in col_names:
            column = Column(name)
            self.columns.append(column)

            # Horizontal einfügen
            column.right = last.right
            column.left = last
            last.right.left = column
            last.right = column
            last = column

        # Matrix befüllen
        for r_idx, row in enumerate(matrix):
            first = None
            for i, cell in enumerate(row):
                if cell == 1:
                    column = self.columns[i]

                    node = Node(r_idx)
                    node.column = column

                    node.down = column
                    node.up = column.up
                    column.up.down = node
                    column.up = node
                    column.size += 1

                    # Horizontale Verbindung innerhalb der Zeile
                    if first is None:
                        first = node
                    else:
                        node.left = first.left
                        node.right = first
                        first.left.right = node
                        first.left = node

    def cover(self, column):
        column.right.left = column.left
        column.left.right = column.right

        row = column.down
        while row != column:
            node = row.right
            while node != row:
                node.down.up = node.up
                node.up.down = node.down
                node.column.size -= 1
                node = node.right
            row = row.down

    def uncover(self, column):
        row = column.up
        while row != column:
            node = row.left
            while node != row:
                node.column.size += 1
                node.down.up = node
                node.up.down = node
                node = node.left
            row = row.up
        column.right.left = column
        column.left.right = column

    def print_state(self):
        count = 0
        curr = self.head.right
        while curr != self.head:
            count += 1
            curr = curr.right
        print(f"Depth: {len(self.solution)} | Active columns: {count}")

    def search(self):
        # self.print_state()
        if self.head.right == self.head:
            yield list(self.solution)
            return

        # Wähle Spalte mit kleinster Anzahl an Zeilen aus (NUR aktive Spalten durchsuchen)
        column = self.head.right
        c = column.right
        while c != self.head:
            if c.size < column.size:
                column = c
            c = c.right

        self.cover(column)

        row = column.down
        while row != column:
            self.solution.append(row)

            node = row.right
            while node != row:
                self.cover(node.column)
                node = node.right

            yield from self.search()

            # Backtrack
            self.solution.pop()
            node = row.left
            while node != row:
                self.uncover(node.column)
                node = node.left
            row = row.down
        self.uncover(column)

def build_exact_cover_matrix(game):
    pieces = game.pieces
    width, height = game.board_w, game.board_h

    col_names = []

    # Eine Spalte pro Feld
    for x in range(width):
        for y in range(height):
            col_names.append(f"{x},{y}")

    # Eine Spalte pro Piece
    piece_col_start = len(col_names)
    for piece in pieces:
        col_names.append(f"{piece.id}")

    matrix = []     # 0/1 reihen
    actions = []    # (piece_id, x, y, rotated?)

    # Für jedes Piece alle möglichen Platzierungen
    for piece in pieces:
        # Beide Ausrichtungen für nicht quadratische Pieces
        orientations = [False]
        if piece.w != piece.h:
            orientations.append(True)

        for rotate in orientations:
            pwidth = piece.h if rotate else piece.w
            pheight = piece.w if rotate else piece.h

            # Alle möglichen Positionen testen
            for x in range(width - pwidth + 1):
                for y in range(height - pheight + 1):
                    if not game.check_collision(piece, x, y, pwidth, pheight):
                        row = [0] * len(col_names)

                        # Board-Felder markieren
                        for dy in range(pheight):
                            for dx in range(pwidth):
                                idx = col_names.index(f"{x+dx},{y+dy}")
                                if idx is not None:
                                    row[idx] = 1
                        row[piece_col_start + piece.id] = 1

                        matrix.append(row)
                        actions.append((piece.id, x, y, rotate))
    return matrix, col_names, actions

def solve(game: PlacementGameCLI.PlacementGame, delay: int = 0):
    start_time = time()
    matrix, col_names, actions = build_exact_cover_matrix(game)
    dl = DancingLinks(matrix, col_names)

    solution_found = False
    solution_count = 0
    for solution in dl.search():
        solution_found = True
        solution_count += 1
        game.reset()
        for node in solution:
            piece_id, x, y, rotate = actions[node.row_id]

            piece = game.pieces[piece_id]

            if piece.placed:
                game.remove(piece_id)

            if rotate and piece.w != piece.h:
                game.rotate(piece_id)

            game.place(piece_id, x, y)
            sleep(delay)
        print("--------------")
        print(f"Solution {solution_count}")
        sleep(delay)

    print(f"Total time: {time() - start_time:.2f}s")

    if not solution_found:
        print("No solution found!")
    else:
        print(f'Number of solutions found: {solution_count}.')

from adt_array import Array
import time
import os

class GameOfLife:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.grid = Array(rows)
        for i in range(rows):
            self.grid[i] = Array(cols)
            self.grid[i].clear(0)

    def set_alive(self, row, col):
        self.grid[row][col] = 1

    def count_neighbors(self, row, col):
        directions = [
            (-1,-1), (-1,0), (-1,1),
            (0,-1),          (0,1),
            (1,-1),  (1,0),  (1,1)
        ]

        count = 0
        for dr, dc in directions:
            r = row + dr
            c = col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                count += self.grid[r][c]
        return count

    def next_generation(self):
        new_grid = Array(self.rows)
        for i in range(self.rows):
            new_grid[i] = Array(self.cols)
            new_grid[i].clear(0)

        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = self.count_neighbors(r, c)

                if self.grid[r][c] == 1:
                    if neighbors == 2 or neighbors == 3:
                        new_grid[r][c] = 1
                else:
                    if neighbors == 3:
                        new_grid[r][c] = 1

        self.grid = new_grid

    def display(self, generation):
        print("\n" * 2)
        print(f"GENERATION : {generation}\n")
        for r in range(self.rows):
            for c in range(self.cols):
                  print("⬛" if self.grid[r][c] == 1 else "⬜", end=" ")
            print()
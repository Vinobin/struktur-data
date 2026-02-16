from game_of_life import GameOfLife
import time

# input ukuran grid
rows = int(input("Masukkan jumlah baris: "))
cols = int(input("Masukkan jumlah kolom: "))

game = GameOfLife(rows, cols)

# pola awal sederhana (blinker di tengah)
mid_r = rows // 2
mid_c = cols // 2

game.set_alive(mid_r - 1, mid_c)
game.set_alive(mid_r, mid_c)
game.set_alive(mid_r + 1, mid_c)

generation = 1

for _ in range(20):
    game.display(generation)
    game.next_generation()
    generation += 1
    time.sleep(0.5)
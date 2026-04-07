import os
import random
import threading
import time
from colorama import Fore, init

init(autoreset=True)

WIDTH = 21
HEIGHT = 11

# ===== Keyboard real-time =====
try:
    import msvcrt
    def get_key():
        return msvcrt.getch().decode('utf-8').lower()
except:
    import sys, tty, termios
    def get_key():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch.lower()

# ===== Generate Maze =====
def generate_maze(width, height):
    maze = [['#' for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        dirs = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0 < nx < height-1 and 0 < ny < width-1 and maze[nx][ny] == '#':
                maze[nx][ny] = '.'
                maze[x + dx//2][y + dy//2] = '.'
                carve(nx, ny)

    maze[1][1] = '.'
    carve(1,1)

    maze[1][1] = 'P'
    maze[height-2][width-2] = 'E'

    return maze

maze = generate_maze(WIDTH, HEIGHT)

player = [1,1]
enemy = [HEIGHT-2, WIDTH-2]

lives = 3
steps = 0
game_over = False

# ===== Tampilkan =====
def tampilkan():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + f"Langkah: {steps} | Nyawa: {lives} ❤️\n")

    for i in range(len(maze)):
        line = ""
        for j in range(len(maze[0])):
            if [i,j] == player:
                line += Fore.GREEN + 'P'
            elif [i,j] == enemy:
                line += Fore.MAGENTA + 'M'
            elif maze[i][j] == '#':
                line += Fore.WHITE + '#'
            elif maze[i][j] == 'E':
                line += Fore.RED + 'E'
            else:
                line += '.'
        print(line)

# ===== Musuh otomatis =====
def enemy_loop():
    global lives, player, game_over

    while not game_over:
        time.sleep(0.4)  # kecepatan musuh (makin kecil makin cepat)

        ex, ey = enemy
        px, py = player

        moves = []
        if px < ex: moves.append((-1,0))
        if px > ex: moves.append((1,0))
        if py < ey: moves.append((0,-1))
        if py > ey: moves.append((0,1))

        random.shuffle(moves)

        for dx, dy in moves:
            nx, ny = ex + dx, ey + dy
            if maze[nx][ny] != '#':
                enemy[0], enemy[1] = nx, ny
                break

        # Cek ketangkep
        if enemy == player:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                player[0], player[1] = 1,1

# Jalankan thread musuh
threading.Thread(target=enemy_loop, daemon=True).start()

# ===== Game Loop Player =====
while True:
    tampilkan()

    if game_over:
        print(Fore.RED + "\n💀 GAME OVER!")
        break

    if maze[player[0]][player[1]] == 'E':
        print(Fore.YELLOW + f"\n🎉 MENANG! Langkah: {steps} | Sisa nyawa: {lives}")
        break

    key = get_key()

    x, y = player

    if key == 'q':
        print("\nKeluar dari game.")
        break
    elif key == 'w':
        nx, ny = x-1, y
    elif key == 's':
        nx, ny = x+1, y
    elif key == 'a':
        nx, ny = x, y-1
    elif key == 'd':
        nx, ny = x, y+1
    else:
        continue

    if maze[nx][ny] != '#':
        player = [nx, ny]
        steps += 1
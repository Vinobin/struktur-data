N = 8

move_x = [2, 1, -1, -2, -2, -1, 1, 2]
move_y = [1, 2, 2, 1, -1, -2, -2, -1]


def is_safe(x, y, board):
    return 0 <= x < N and 0 <= y < N and board[x][y] == -1


def print_board(board):
    for row in board:
        for cell in row:
            print(f"{cell:2}", end=" ")
        print()


def get_degree(x, y, board):
    count = 0
    for i in range(8):
        nx = x + move_x[i]
        ny = y + move_y[i]

        if is_safe(nx, ny, board):
            count += 1

    return count


def solve_knight_tour(board, x, y, movei):
    if movei == N * N:
        return True

    next_moves = []

    for i in range(8):
        nx = x + move_x[i]
        ny = y + move_y[i]

        if is_safe(nx, ny, board):
            degree = get_degree(nx, ny, board)
            next_moves.append((degree, nx, ny))

    next_moves.sort()

    for _, nx, ny in next_moves:
        board[nx][ny] = movei

        if solve_knight_tour(board, nx, ny, movei + 1):
            return True

        board[nx][ny] = -1

    return False


start_x = int(input("Masukkan posisi awal X (0-7): "))
start_y = int(input("Masukkan posisi awal Y (0-7): "))

board = [[-1 for _ in range(N)] for _ in range(N)]

board[start_x][start_y] = 0

if solve_knight_tour(board, start_x, start_y, 1):
    print("\nSolusi ditemukan:\n")
    print_board(board)
else:
    print("Tidak ada solusi.")
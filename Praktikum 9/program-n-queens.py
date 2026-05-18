def print_board(board, n):
    for i in range(n):
        for j in range(n):
            if board[i] == j:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()
    print()

def is_safe(board, row, col):
    for i in range(row):
        
        if board[i] == col:
            return False

        
        if abs(board[i] - col) == abs(i - row):
            return False

    return True


def solve_n_queens(board, row, n):
    if row == n:
        return True

    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col

            if solve_n_queens(board, row + 1, n):
                return True

            board[row] = -1

    return False


n = int(input("Masukkan ukuran papan N: "))

board = [-1] * n

if solve_n_queens(board, 0, n):
    print("\nSolusi ditemukan:\n")
    print_board(board, n)
else:
    print("Tidak ada solusi.")
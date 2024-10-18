import random

def easy_ai(board):
    moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]
    return random.choice(moves) if moves else None

def medium_ai(board , Player):
    # Vérifier les lignes
    for i in range(3):
        if board[i].count(Player) == 2 and board[i].count(None) == 1:
            j = board[i].index(None)
            return (i, j)

    # Vérifier les colonnes
    for j in range(3):
        col = [board[i][j] for i in range(3)]
        if col.count(Player) == 2 and col.count(None) == 1:
            i = col.index(None)
            return (i, j)

    # Vérifier les diagonales
    diag1 = [board[i][i] for i in range(3)]
    if diag1.count(Player) == 2 and diag1.count(None) == 1:
        i = diag1.index(None)
        return (i, i)

    diag2 = [board[i][2 - i] for i in range(3)]
    if diag2.count(Player) == 2 and diag2.count(None) == 1:
        i = diag2.index(None)
        return (i, 2 - i)

    # Sinon, jouer un coup facile
    return easy_ai()

def hard_ai(Player,Bot,board):
    def minimax(board, depth, is_maximizing):
        winner, _ = is_win()
        if winner == Bot:
            return 1
        elif winner == Player:
            return -1
        elif is_full():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = Bot
                        score = minimax(board, depth + 1, False)
                        board[i][j] = None
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = Player
                        score = minimax(board, depth + 1, True)
                        board[i][j] = None
                        best_score = min(score, best_score)
            return best_score

    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = Bot
                score = minimax(board, 0, False)
                board[i][j] = None
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def is_win(board):
    for i in range(3):
        if board[i][0] is not None and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0], [(i, 0), (i, 1), (i, 2)]

    for j in range(3):
        if board[0][j] is not None and board[0][j] == board[1][j] == board[2][j]:
            return board[0][j], [(0, j), (1, j), (2, j)]

    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2], [(0, 2), (1, 1), (2, 0)]

    return None, []

def is_full(board):
    return all(cell is not None for row in board for cell in row)
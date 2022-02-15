import random

class Engine():
    def __init__(self, board=None, turn=None) -> None:
        self.board = [[0 for _ in range(7)] for __ in range(6)] if board is None else board
        self.turn = 1 if turn is None else turn
        self.depth = 5

    def reset(self) -> None:
        self.turn = 1
        self.board = [[0 for _ in range(7)] for __ in range(6)]

    def is_valid(self, s) -> bool:
        i, j = s[0], s[1]
        try:
            if self.board[i][j] == 0:
                if i == 5:
                    return True
                else:
                    if self.board[i + 1][j] in (1, -1):
                        return True
        except IndexError:
            return False
        return False

    def is_draw(self) -> bool:
        for i in range(6):
            for j in range(7):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def check_for_winner(self) -> int:
        for i in range(6):
            for j in range(7):
                if self.board[i][j] in (1, -1):
                    if i <= 2 and (self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j]):
                        return self.board[i][j]
                    elif i >= 3 and (self.board[i][j] == self.board[i - 1][j] == self.board[i - 2][j] == self.board[i - 3][j]):
                        return self.board[i][j]
                    elif j <= 3 and (self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3]):
                        return self.board[i][j]
                    elif j >= 3 and self.board[i][j] == self.board[i][j - 1] == self.board[i][j - 2] == self.board[i][j - 3]:
                        return self.board[i][j]
                    elif i <= 2 and j <= 3 and (self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == self.board[i + 3][j + 3]):
                        return self.board[i][j]
                    elif i >= 3 and j >= 3 and (self.board[i][j] == self.board[i - 1][j - 1] == self.board[i - 2][j - 2] == self.board[i - 3][j - 3]):
                        return self.board[i][j]
                    elif i <= 2 and j >= 3 and (self.board[i][j] == self.board[i + 1][j - 1] == self.board[i + 2][j - 2] == self.board[i + 3][j - 3]):
                        return self.board[i][j]
                    elif i >= 3 and j <= 3 and (self.board[i][j] == self.board[i - 1][j + 1] == self.board[i - 2][j + 2] == self.board[i - 3][j + 3]):
                        return self.board[i][j]
        return 0

    def make_move(self, s) -> bool:
        if self.is_valid(s):
            i, j = s[0], s[1]
            self.board[i][j] = self.turn
            self.turn *= -1
            return True
        return False

    def get_all_valid_moves(self) -> list:
        valid_moves = []
        for i in range(6):
            for j in range(7):
                if self.is_valid((i, j)):
                    valid_moves.append((i, j))
        return valid_moves

    def get_best_move(self) -> tuple:
        self.opponent = self.turn * -1
        return self.minimax(self.depth, -10000000, 10000000, True)[1]

    def minimax(self, depth, alpha, beta, is_maximising) -> list:
        all_valid_moves = self.get_all_valid_moves()
        random.shuffle(all_valid_moves)
        winner = self.check_for_winner()
        is_draw = self.is_draw()
        
        if depth == 0 or (winner in (1, -1) or is_draw):
            if winner == self.turn:
                return 10000, None
            elif winner == self.opponent:
                return -10000, None
            elif is_draw:
                return 0, None
            else:
                return self.heuristic(), None

        if is_maximising:
            best_score = -100000
            best_move = None
            for move in all_valid_moves:
                self.board[move[0]][move[1]] = self.turn
                score = self.minimax(depth - 1, alpha, beta, False)[0]
                self.board[move[0]][move[1]] = 0
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            return best_score, best_move

        else:
            best_score = 100000
            best_move = None
            for move in all_valid_moves:
                self.board[move[0]][move[1]] = self.opponent
                score = self.minimax(depth - 1, alpha, beta, True)[0]
                self.board[move[0]][move[1]] = 0
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
            return best_score, best_move

    def heuristic(self) -> int:
        score = 0
        for i in range(6):
            if self.board[i][3] == self.turn:
                score += 100
            elif self.board[i][3] == self.opponent:
                score -= 100

        if self.board[0][0] == self.turn or self.board[0][6] == self.turn or self.board[5][0] == self.turn or self.board[5][6] == self.turn:
            score += 10
        if self.board[0][0] == self.opponent or self.board[0][6] == self.opponent or self.board[5][0] == self.opponent or self.board[5][6] == self.opponent:
            score -= 10

        for i in range(6):
            for j in range(7):
                n = 1 if self.board[i][j] == self.turn else -1
                if i <= 4 and (self.board[i][j] == self.board[i + 1][j] != 0) and (self.is_valid((i + 2, j)) or self.is_valid((i - 1, j))):
                    score += n * 50
                if i <= 3 and (self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] != 0) and (self.is_valid((i + 3, j)) or self.is_valid((i - 1, j))):
                    score += n * 100
                if i >= 1 and (self.board[i][j] == self.board[i - 1][j] != 0) and (self.is_valid((i - 2, j)) or self.is_valid((i + 1, j))):
                    score += n * 50
                if i >= 2 and (self.board[i][j] == self.board[i - 1][j] == self.board[i - 2][j] != 0) and (self.is_valid((i - 3, j)) or self.is_valid((i + 1, j))):
                    score += n * 100
                if j <= 5 and (self.board[i][j] == self.board[i][j + 1] != 0) and (self.is_valid((i, j + 2))):
                    score += n * 50
                if j <= 4 and (self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] != 0) and (self.is_valid((i, j + 3))):
                    score += n * 100
                if i <= 4 and j <= 5 and (self.board[i][j] == self.board[i + 1][j + 1] != 0) and (self.is_valid((i + 2, j + 2))):
                    score += n * 50
                if i <= 3 and j <= 3 and (self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] != 0) and (self.is_valid((i + 3, j + 3))):
                    score += n * 100
                if i >= 1 and j >= 1 and (self.board[i][j] == self.board[i - 1][j - 1] != 0) and (self.is_valid((i - 2, j - 2))):
                    score += n * 50
                if i >= 2 and j >= 2 and (self.board[i][j] == self.board[i - 1][j - 1] == self.board[i - 2][j - 2] != 0) and (self.is_valid((i - 3, j - 3))):
                    score += n * 100
                if i <= 4 and j >= 1 and (self.board[i][j] == self.board[i + 1][j - 1] != 0) and (self.is_valid((i + 2, j - 2))):
                    score += n * 50
                if i <= 3 and j <= 4 and (self.board[i][j] == self.board[i + 1][j - 1] == self.board[i + 2][j - 2] != 0) and (self.is_valid((i + 3, j - 3))):
                    score += n * 100
                if i >= 1 and j <= 5 and (self.board[i][j] == self.board[i - 1][j + 1] != 0) and (self.is_valid((i - 2, j + 2))):
                    score += n * 50
                if i >= 2 and j <= 4 and (self.board[i][j] == self.board[i - 1][j + 1] == self.board[i - 2][j + 2] != 0) and (self.is_valid((i - 3, j + 3))):
                    score += n * 100
        return score
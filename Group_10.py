#====================================================================================================#
# Imports:                                                                                           #
#====================================================================================================#

from typing import Any, List, Tuple

#====================================================================================================#
# Play Function:                                                                                     #
#====================================================================================================#

def play(board:List[List[int]], choices:List[int], player:int, memory:Any) -> Tuple[int, Any]:
    
    n_rows = len(board)
    
            
    def calculate_board_score(board, player):
       
        # Adjust based on the actual size of the board. Aiming for long chains.
        def score_consecutive(count, current_player):
            if current_player == player:
                if count == 2: return 3
                elif count == 3: return 10
                elif count == 4: return 30
                elif count == 5: return 100
                elif count == 6: return 300
                elif count == 7: return 500
            else:
                # Penalize opponent's chains to block them
                if count == 2: return -5
                elif count == 3: return -15
                elif count == 4: return -45
                elif count == 5: return -150
                elif count == 6: return -350
                elif count == 7: return -550
            return 0

        # Check cell helper
        def check_cell(i, j, last, count):
            if j >= len(board[i]):
                last, count = -1, 0
            elif board[i][j] == last:
                count = count + 1
            else:
                last, count = board[i][j], 1
            return last, count

        score = 0

        #Center position
        center_array = board[len(board)//2]
        center_count = center_array.count(player)
        score += center_count * 5

        # Vertically
        for i in range(len(board)):
            last, count = -1, 0
            for j in range(n_rows):
                last, count = check_cell(i, j, last, count)
                score += score_consecutive(count, last)
                 
        # Horizontally
        for j in range(n_rows):
            last, count = -1, 0
            for i in range(len(board)):
                last, count = check_cell(i, j, last, count)
                score += score_consecutive(count, last)

        # Diagonal up-right
        for i in range(len(board)):
            j, last, count = 0, -1, 0
            while i < len(board) and j < n_rows:
                last, count = check_cell(i, j, last, count)
                score += score_consecutive(count, last)
                i += 1
                j += 1

        for j in range(len(board)):
            i, last, count = 0, -1, 0
            while i < len(board) and j < n_rows:
                last, count = check_cell(i, j, last, count)
                score += score_consecutive(count, last)
                i += 1
                j += 1

        # Diagonal down-left
        for i in range(len(board)):
            j, last, count = n_rows - 1, -1, 0
            while i < len(board) and j >= 0:
                last, count = check_cell(i, j, last, count)
                score += score_consecutive(count, last)
                i += 1
                j -= 1

        for j in range(len(board)):
            i, last, count = len(board) - 1, -1, 0
            while i >= 0 and j < n_rows:
                last, count = check_cell(i, j, last, count)
                score += score_consecutive(count, last)
                i -= 1
                j += 1
        
        return score


    def drop_piece(board, col, player):
        board[col].append(player) 

    def reflect_board(board):
        reflected_board = []
        for _ in range(len(board)):
            reflected_board.append([])
        for i in range(len(board)):
            for j in range(len(board[i])):
                reflected_board[i].append(board[i][j])
        return reflected_board

    def minimax(board, depth, is_max, player, choices, alpha, beta):
        
        opponent = 1 if player == 0 else 0
        player_score = calculate_board_score(board, player)
        opponent_score = calculate_board_score(board, opponent)
        
        if depth == 0 or choices == []:
            return (None, player_score - opponent_score) 
        if is_max:
            max_score = float('-inf')
            column = choices[len(choices)//2]
            for col in choices:
                temp_board = reflect_board(board)
                drop_piece(temp_board, col, player)
                max_eval = minimax(temp_board, depth-1, False, player, choices, alpha, beta)[1]
                if max_eval > max_score:
                    max_score = max_eval
                    column = col 
                alpha = max(alpha, max_score)
                if beta <= alpha:
                    break
            return column, max_score

        else:
            min_score = float('inf')
            column = choices[len(choices)//2]
            for col in choices:
                temp_board = reflect_board(board)
                drop_piece(temp_board, col, opponent)
                min_eval = minimax(temp_board, depth-1, False, player, choices, alpha, beta)[1]
                if min_eval < min_score:
                    min_score = min_eval
                    column = col 
                beta = min(beta, min_score)
                if beta <= alpha:
                    break
            return column, min_score

    move, _ = minimax(board, 2, True, player, choices, float('-inf'), float('inf'))
    
    return move, memory
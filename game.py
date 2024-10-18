import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from bot_ai import easy_ai , hard_ai , medium_ai , is_win , is_full
app = Flask(__name__)
CORS(app, supports_credentials=True)


board = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]


Bot = None
Player = None


mode = None
current_turn = None
firstBotMove = False

@app.route('/pick_mode', methods=['POST'])
def random_pick():
    global Player, Bot, mode, current_turn, firstBotMove, board
    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]
    if request.json and 'mode' in request.json:
        mode = request.json['mode']
    else:
        return jsonify({'error': 'Mode not provided'}), 400

    Player = random.choice(['X', 'O'])
    Bot = 'O' if Player == 'X' else 'X'
    current_turn = random.choice([Player, Bot])

    print("Bot :", Bot, "et Player :", Player)  # debug
    print("Le tour de :", current_turn)  # debug

    response = {
        'player': Player,
        'bot': Bot,
        'currentTurn': current_turn
    }

    if current_turn == Bot:
        print("C'est le tour du bot !")
        firstBotMove = True
        print("Le mode choisi :", mode)
        bot_move = choose_bot_move(mode)
        print("Le premier coup du bot :", bot_move)
        if bot_move:
            i, j = bot_move
            board[i][j] = Bot
            current_turn = Player  
            response.update({
                'bot_move': {'i': i, 'j': j},
                'currentTurn': current_turn  
            })
        else:
            return jsonify({'error': 'No valid moves available'}), 500
        print("Le plateau après le premier coup du bot :", board)
        firstBotMove = False

    return jsonify(response)



@app.route('/move', methods=['POST'])
def move():
    global current_turn, firstBotMove, mode
    data = request.json
    i, j, turn = data.get('i'), data.get('j'), data.get('turn')  # Getting info from the post
    print("le i et j depalcement du player",i, j)  # debug
    if i is None or j is None or not (0 <= i < 3) or not (0 <= j < 3):
        return jsonify({'error': 'Invalid indices provided'}), 400  # Checking for the i and j
    if board[i][j] is not None:
        return jsonify({'error': 'Cell already taken'}), 400
    if turn == Player:
        board[i][j] = Player
        current_turn = Bot
        winner, winning_line = is_win(board)
        response = {'currentTurn': current_turn}
        if winner:
            response.update({'winner': winner, 'winning_line': winning_line})
        if is_full(board):
            response.update({'draw': True})
        if winner or is_full(board):
            return jsonify(response)
        
        # Bot doit jouer
        bot_move = choose_bot_move(mode)
        if bot_move:
            bi, bj = bot_move
            print("le tour du bot apres le player" , bi, bj)  # debug
            board[bi][bj] = Bot
            winner, winning_line = is_win(board)  
            current_turn = Player
            response.update({'bot_move': {'i': bi, 'j': bj}, 'board': board, 'currentTurn': current_turn})
            if winner:
                response.update({'winner': winner, 'winning_line': winning_line})
            if is_full(board):
                response.update({'draw': True})
        else:
            return jsonify({'error': 'No valid moves available'}), 500

        print(" apres avoir jouer le bot apres le player" , board)
        return jsonify(response)
    else:
        return jsonify({'error': 'Not your turn'}), 400

def choose_bot_move(mode):
    global firstBotMove
    if mode == 'Easy' or firstBotMove: 
        return easy_ai(board)
    elif mode == 'Medium': 
        return medium_ai(board,Player)
    else:
        return hard_ai(Player,Bot,board)

@app.route('/reset', methods=['POST'])
def reset_board():
    global board, current_turn
    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]
    current_turn = None
    return jsonify({'message': 'Board reset successfully'})


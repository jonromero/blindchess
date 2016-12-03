from flask import Flask
from flask import request, render_template
from sunfish.sunfish import *

app = Flask(__name__)

pos = Position(initial, 0, (True,True), (True,True), 0, 0)
searcher = Searcher()
all_moves = ''
steps = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    global pos
    global searcher
    global all_moves
    global steps
    
    if pos.score <= -MATE_LOWER:
        computer_move = "You lost"
        
    if request.method == 'POST':
        move = request.form['move'].lower()
        while move not in pos.gen_moves():
            match = re.match('([a-h][1-8])'*2, move)
            if match:
                all_moves += str(steps)+'. ' + move + ' '
                move = parse(match.group(1)), parse(match.group(2))
            else:
                # Inform the user when invalid input (e.g. "help") is entered
                computer_move = "Please enter a valid move"
        pos = pos.move(move)
        if pos.score <= -MATE_LOWER:
            computer_move = "You won"

        move, score = searcher.search(pos, secs=2)

        computer_move = str(render(119-move[0]) + render(119-move[1]))
        pos = pos.move(move)
        steps += 1
        
        if score == MATE_UPPER:
            computer_move = "Checkmate"

        all_moves += computer_move + ' '

    last_move = all_moves.split(" ")[-2] if all_moves != '' else ''
    return render_template('index.html', moves=all_moves, move=last_move)


    
@app.route('/reset', methods=['GET'])
def reset():
    global pos
    global searcher
    global all_moves
    global steps
    
    pos = Position(initial, 0, (True,True), (True,True), 0, 0)
    searcher = Searcher()
    all_moves = ''
    steps = 1

    return "reset"

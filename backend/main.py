from flask import Flask, request, jsonify
from mine_sweeper_board import MineSweeperBoard

app = Flask(__name__)

# Initialize the board globally
board = None

def check_initialize_params(data):
    if 'size' not in data or 'first_click' not in data:
        return False, "Missing required parameters: 'size' and 'first_click'"
    return True, ""

def check_place_mines_params(data):
    if 'position' not in data:
        return False, "Missing required parameter: 'position'"
    return True, ""

@app.route('/initialize_board', methods=['POST'])
def initialize_board():
    global board
    data = request.get_json()

    # Check parameters
    is_valid, message = check_initialize_params(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    size = data.get('size')
    first_click = tuple(data.get('first_click'))
    board = MineSweeperBoard(size, first_click)
    return jsonify({"message": "Board initialized", "size": size, "first_click": first_click}), 200

@app.route('/place_mines', methods=['POST'])
def place_mines():
    global board
    if board is None:
        return jsonify({"error": "Board not initialized"}), 400

    data = request.get_json()

    # Check parameters
    is_valid, message = check_place_mines_params(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    position = tuple(data.get('position'))
    board.place_mines(position)
    return jsonify({"message": "Mines placed", "position": position}), 200

if __name__ == '__main__':
    app.run(debug=True)

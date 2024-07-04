from flask import Flask, request, jsonify
from flask_cors import CORS
from mine_sweeper_board import MineSweeperBoard
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

CORS(app)

# Initialize the board globally
game = None

def check_initialize_params(data):
    if 'width' not in data or 'height' not in data or 'numMines' not in data:
        return False, "Missing required parameters"
    return True, ""

def check_place_mines_params(data):
    if 'firstClickLocation' not in data:
        return False, "Missing required parameter"
    return True, ""

@app.route('/initialize_board', methods=['POST'])
def initialize_board():
    
    global game
    data = request.get_json()

    # Check parameters
    is_valid, message = check_initialize_params(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    grid_height = data.get('height')
    grid_width = data.get('width')
    num_mines = data.get('numMines')
    grid_size = (grid_height, grid_width)
    game = MineSweeperBoard(num_mines=num_mines, grid_size=grid_size)
    
    return jsonify({"message": "Board initialized", "size": (grid_height, grid_width), "numMines": num_mines}), 200

@app.route('/place_mines', methods=['POST'])
def place_mines():
    global game
    if game is None:
        return jsonify({"error": "Board not initialized"}), 400

    data = request.get_json()

    # Check parameters
    is_valid, message = check_place_mines_params(data)
    if not is_valid:
        return jsonify({"error": message}), 400

    first_click_location = tuple(data.get('firstClickLocation'))
    game.place_mines(first_click_location)
    
    
    return jsonify({"message": "Mines placed.", "board": game.board, "firstClickLocation": first_click_location}), 200

if __name__ == '__main__':
    app.run(debug=True)

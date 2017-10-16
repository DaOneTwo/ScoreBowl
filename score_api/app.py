from flask import Flask, abort, jsonify, make_response, request

from score_api.objects.game import GameController

games = {}

app = Flask(__name__)

@app.route('/CreateGame', methods=['POST'])
def create_game():
    """initialize a new bowling game"""
    game = GameController()
    games[game.game_id] = game

    return jsonify(game.game_state())

@app.route('/<game_id>/AddPlayer', methods=['PUT'])
def add_player(game_id):
    """add a player to an exiting game"""
    # get the game object
    game = games.get(game_id)
    name = request.json['name']
    if not all([game, request.json, name]):
        abort(400)

    return jsonify(game.add_player(name))

@app.route('/<game_id>/StartGame', methods=['POST'])
def start_game(game_id):
    """start the game_id"""
    game = games.get(game_id)
    if not game:
        abort(400)

    return jsonify(game.start_game())

@app.route('/<game_id>/ScoreRoll', methods=['POST'])
def score_roll(game_id):
    """score a roll on the given game"""
    game = games.get(game_id)
    pins_down = request.json['downed_pins']
    if not all([game, request.json, isinstance(pins_down, int), pins_down >= 0]):
        abort(400)

    return jsonify(game.score_roll(pins_down))


if __name__ == '__main__':
    app.run(debug=True)
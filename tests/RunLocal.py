import random
import requests
from urllib.parse import urljoin


def get_n_print_response_info(response):
    print(response.status_code)
    print(response.json())

    return response.json()

def get_uris_from_json(response_json):
    return response_json['uris']

def get_roll_data(resp_json):

    advance = resp_json.get('roll_results', {}).get('advance_player')
    next_player = resp_json.get('next_player')
    next_frame = resp_json.get('next_frame')
    next_roll = resp_json.get('next_roll_number')
    running_total = resp_json.get('roll_results', {}).get('player_running_score')
    game_complete = resp_json.get('game_complete')

    return advance, next_player, next_frame, next_roll, running_total, game_complete

base_url = 'http://127.0.0.1:5000/'

# CREATE A GAME
r1 = requests.post(url=urljoin(base_url, 'CreateGame'))
r1_json = get_n_print_response_info(r1)
add_player_uri = get_uris_from_json(r1_json).get('add_player')

# ADD PLAYER(S)
players = ['Andy', 'April']
for player in players:
    pp = requests.put(add_player_uri, json={'name': player})
    pp_json = get_n_print_response_info(pp)

start_game_uri = get_uris_from_json(pp_json).get('start_game')

# START THE GAME
sg = requests.post(start_game_uri)
sg_json = get_n_print_response_info(sg)

score_roll_uri = get_uris_from_json(sg_json).get('score_roll')

next_player = sg_json.get('next_player')
game_complete = False
valid_rolls = [i for i in range(0, 11)]
while not game_complete:
    roll1 = random.choice(valid_rolls)

    print(f'{next_player} rolls a {roll1}')

    rp = requests.post(score_roll_uri, json={'downed_pins': roll1})
    rp_json = get_n_print_response_info(rp)

    old_player = next_player
    advance, next_player, next_frame, next_roll, running_total, game_complete = get_roll_data(rp_json)

    print(f'{old_player}\'s running total {running_total}')
    if game_complete:
        print('\n Game Complete!!\n')
        [print(i) for i in rp1_json['final_scores']]

    while not advance:
        if next_roll != 3:
            v_rolls = [i for i in range(0, 11 - roll1)]
        else:
            v_rolls = valid_rolls
        r2_value = random.choice(v_rolls)
        rp1 = requests.post(score_roll_uri, json={'downed_pins': r2_value})
        print(f'{next_player} rolls a {r2_value}')
        rp1_json = get_n_print_response_info(rp1)
        advance, next_player, next_frame, next_roll, running_total, game_complete = get_roll_data(rp1_json)
        print(f'{old_player} running total {running_total}')

        if game_complete:
            print('\n Game Complete!!\n')
            [print(i) for i in rp1_json['final_scores']]
















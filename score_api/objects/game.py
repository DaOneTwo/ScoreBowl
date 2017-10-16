from flask import url_for
from secrets import token_urlsafe

from score_api.objects.player import Player


class GameController(object):
    """A controller for a multi player Bowling Game.  Aims to sim"""
    def __init__(self, frames=10):
        """Initialize a bowling game"""
        self.game_id = token_urlsafe(32)
        self.uris = {'add_player': url_for('add_player', game_id=self.game_id, _external=True)}
        self.started = False
        self.players = []
        self.frames = frames

        self.frame_index = None
        self.player_index = None
        self.roll_count = 1

    def add_player(self, name: str):
        """add a player to the game with an empty scorecard"""
        self.players.append(Player(name=name))
        self.uris['start_game'] = url_for('start_game', game_id=self.game_id, _external=True)

        return self.game_state()

    def start_game(self):
        """Mark the game as started and so some prep work"""
        # start over with the uris
        self.uris = {'score_roll': url_for('score_roll', game_id=self.game_id, _external=True)}
        self.started = True

        self.frame_index = 1
        self.player_index = 0

        resp_data = self.game_state()
        resp_data['next_player'] = self.players[self.player_index].name
        resp_data['next_frame'] = self.frame_index
        resp_data['next_roll'] = self.roll_count

        return resp_data

    def game_state(self):
        """return the current state of the game as a dict."""
        return {'started': self.started,
                'players': [player.name for player in self.players],
                'game_id': self.game_id,
                'uris': self.uris}

    def score_roll(self, pins_downed):
        """score a roll according to the current player and frame index and advance as necessary"""
        # get the players scorecard.
        scorecard = self.players[self.player_index].scorecard
        details = scorecard.add_roll(pins_downed)
        self.roll_count += 1

        # add the player name to the details returned for the roll
        details['player_name'] = self.players[self.player_index].name
        complete = False

        if details.get('advance_player') is True:
            complete = self._advance_frame_and_player_index()
        if complete:
            return self.complete_game(details)

        else:
            resp_dict = self.game_state()
            resp_dict['game_complete'] = complete


            return {

                    'game_complete': complete,
                    'next_player': self.players[self.player_index].name,
                    'next_frame': self.frame_index,
                    'next_roll_number': self.roll_count,
                    'roll_results': details,
                    'game_data': self._get_game_data(),
                    'uris': self.uris
                    }


    def complete_game(self, details:dict):
        """return a game complete response.  requires the dictionary of roll results"""
        return {'game_id': self.game_id,
                'game_complete': True,
                'final_scores': self._get_final_scores(),
                'next_player': None,
                'next_frame': None,
                'next_roll_number': None,
                'roll_results': details,
                'game_data': self._get_game_data(),
                'uris': None
                }

    def _get_final_scores(self):
        return [f'{player.name} : {player.scorecard.get_running_total()}' for player in self.players]

    def _advance_frame_and_player_index(self) -> bool:
        """advance the frame and player indexes and reset a roll count according to needs.
        returns a bool indicating the game is complete
        """
        if self.player_index == len(self.players) - 1:
            # last player in list we advance frame index and reset player index to 0
            self.frame_index += 1
            self.player_index = 0
            self.roll_count = 1
        else:
            self.player_index += 1
            self.roll_count = 1


        return bool(self.frame_index > self.frames)

    def _get_game_data(self):
        """return all current game data for all players"""

        return [{'name': player.name,
                 'scorecard': [frame.__dict__() for frame in player.scorecard.frames]
                 }
                for player in self.players]


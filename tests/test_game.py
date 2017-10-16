from score_api.objects import game



# class TestGameFlow(object):
#     _game = game.GameController(frames=10)
#
#     def test_add_player(self):
#         """test adding a player to the game"""
#         name = 'Andy'
#         response = self._game.add_player(name)
#         assert(len(response.get('players') == 1))
#         assert(len(self._game.players) == 1)
#         assert(self._game.started is False)
#         assert(self._game.players[0].name == name)
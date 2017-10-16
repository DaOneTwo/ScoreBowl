from score_api.objects.scorecard import GameScorecard


class Player(object):
    def __init__(self, name:str, frames:int=10):
        self.name = name
        self.scorecard = GameScorecard(max_frames=frames)

    def __dict__(self):
        return {'name': self.name,
                'scorecard': [frame.__dict__() for frame in self.scorecard.frames]}


    def __str__(self):
        return self.name
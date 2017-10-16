
import score_api.objects.frames as frame

class GameScorecard(object):
    def __init__(self, max_frames=10):
        self.max_frames = max_frames
        self.frames = []
        self.running_total = 0
        self.game_complete = False

        # add our initial frame
        if max_frames == 1:
            self.frames.append(frame.FinalFrame())
        else:
            self.frames.append(frame.StandardFrame())

    def add_roll(self, pins_down):
        """add a roll to the scorecard.  Will add frames to to the scorecard as necessary until the game is
        complete (max_frames played)"""
        if self.game_complete is True:
            raise Exception('Game complete cannot add a roll')

        frame = self.frames[-1]
        if frame.frame_complete() is True:
            frame = self.add_frame()
        frame_details = frame.add_roll_score(pins_down)

        self.get_running_total()
        self.game_complete = bool(len(self.frames) == self.max_frames and frame.frame_complete())

        return {'advance_player': frame_details.get('frame_complete'),
                'player_running_score': self.running_total,
                'player_game_complete': self.game_complete,
                'player_scorecard_details': [frame_detail.__dict__() for frame_detail in self.frames]}

    def add_frame(self) -> frame.StandardFrame or frame.FinalFrame:
        """Add a frame object to the scorecard"""
        current_length = len(self.frames)
        if current_length < self.max_frames - 1:
            self.frames.append(frame.StandardFrame())
        elif current_length == self.max_frames - 1:
            self.frames.append(frame.FinalFrame())
        else:
            raise Exception('game complete')

        return self.frames[-1]

    def get_frame(self, frame_index, allow_faked=False) -> frame.StandardFrame or frame.FinalFrame:
        """get the frame object by the index passed in.  Index should be the  no zero based index."""
        try:
            return self.frames[frame_index - 1]
        except Exception:
            if frame_index > self.max_frames - 1 and allow_faked is not True:
                raise ValueError('No such frame in this game.')
            else:
                # return an empty frame just so we can evaluate as a frame without breaking things.
                return frame.StandardFrame()

    def get_running_total(self):
        """get the running total"""
        self.running_total = 0
        for index, frame in enumerate(self.frames, 1):
            score = frame.frame_score
            if score is not None:
                self.running_total += score
            else:
                try:
                    if index == self.max_frames:
                        if frame.is_strike:
                            frame.score_frame(bonus_one=frame.roll_two, bonus_two=frame.roll_three)
                        elif frame.is_spare:
                            frame.score_frame(bonus_one=frame.roll_three)
                    else:
                        roll_1, roll_2 = None, None
                        if frame.is_strike or frame.is_spare:
                            next_frame = self.get_frame(index + 1)
                            roll_1 = next_frame.roll_one
                            roll_2 = next_frame.roll_two
                        if frame.is_strike and roll_2 is None:
                            next = self.get_frame(index + 2)
                            roll_2 = next.roll_one
                        frame.score_frame(bonus_one=roll_1, bonus_two=roll_2)
                        self.running_total += frame.frame_score
                except:
                    #ToDo: Deal better here
                    pass

        return self.running_total
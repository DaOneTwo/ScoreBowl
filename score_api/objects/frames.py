
class StandardFrame(object):
    def __init__(self):
        self.roll_one = None
        self.roll_two = None

        self.is_strike = False
        self.is_spare = False

        self.frame_score = None

    def was_a_strike(self) -> bool:
        """Determine if the frame produced a strike"""
        return bool(self.roll_one == 10)

    def was_a_spare(self) -> bool:
        """Determine if the frame produced a spare"""
        is_spare = False
        if all([self.roll_one is not None, self.roll_two is not None]):
            is_spare = bool((self.roll_one + self.roll_two) == 10)

        return is_spare

    def frame_complete(self) -> bool:
        """Determine if the frame is complete for this bowler.  Complete meaning all rolls have been made"""
        strike, spare = self.is_strike, self.is_spare
        complete = False
        if any([strike, spare, bool(self.roll_one is not None and self.roll_two is not None)]):
            complete = True

        return complete

    def add_roll_score(self, pins_knocked_down) -> None:
        """Add a roll score and if possible total up our frame.  Set is_strike and is_spare attrs accordingly"""
        if self.roll_one is None:
            self.roll_one = pins_knocked_down
            self.is_strike = self.was_a_strike()
        elif self.roll_two is None and not self.is_strike:
            self.roll_two = pins_knocked_down
            self.is_spare = self.was_a_spare()
        else:
            raise ValueError('Frame not eligible for additional rolls')

        if self.frame_complete() and all([self.is_strike is False, self.is_spare is False]):
            self.score_frame()

        return self.__dict__()

    def score_frame(self, bonus_one:int=None, bonus_two:int=None):
        """Score the frame if we have what we need"""
        if self.frame_score:
            return False, 'Frame has already successfully been scored. No alterations are possible.'

        if all([self.is_strike, bonus_one is not None and bonus_two is not None]):
            self.frame_score = self.roll_one + bonus_one + bonus_two
        elif all([self.is_spare, bonus_one is not None]):  # bonus_two passed will be ignored...
            self.frame_score = self.roll_one + self.roll_two + bonus_one
        elif all([not self.is_strike, not self.is_spare, self.roll_one is not None, self.roll_two is not None]):
            self.frame_score = self.roll_one + self.roll_two
        else:
            return False, 'Unable to score frame with values provided.'

        return True, self.frame_score

    def __dict__(self):
        """get a dictionary representation of our frame object."""
        return {'roll_one': self.roll_one,
                'roll_two': self.roll_two,
                'is_strike': self.is_strike,
                'is_spare': self.is_spare,
                'frame_score': self.frame_score,
                'frame_complete': self.frame_complete()}


class FinalFrame(StandardFrame):
    def __init__(self):
        super().__init__()

        self.roll_three = None  # will be utilized if is spare or is strike

    def frame_complete(self):
        """"""
        complete = False
        if any([self.is_strike, self.is_spare]) and self.roll_three is not None:
            complete = True
        elif all([not self.is_strike, not self.is_spare, self.roll_one is not None, self.roll_two is not None]):
            complete = True

        return complete

    def add_roll_score(self, pins_knocked_down):
        """Add roll score"""
        if self.roll_one is None:
            self.roll_one = pins_knocked_down
            self.is_strike = self.was_a_strike()
        elif self.roll_two is None:
            self.roll_two = pins_knocked_down
            if not self.is_strike:
                self.is_spare = self.was_a_spare()
            else:  # cannot be a spare if it is a strike
                self.is_spare = False
        elif all([self.roll_three is None , any([self.is_strike, self.is_spare])]):
            self.roll_three = pins_knocked_down
            # passing roll_three as the bonus roll one and roll_two as bonus_two will allow just one function
            # call to cover scoring the tenth frame as a strike or a spare with the way the score_frame call
            # works (ignoring bonus_two when passed.
            self.score_frame(bonus_one=self.roll_three, bonus_two=self.roll_two)

        return self.__dict__()

    def __dict__(self):
        """get a dictionary representation of our frame object."""
        return {'roll_one': self.roll_one,
                'roll_two': self.roll_two,
                'roll_three': self.roll_three,
                'is_strike': self.is_strike,
                'is_spare': self.is_spare,
                'frame_score': self.frame_score,
                'frame_complete': self.frame_complete()}
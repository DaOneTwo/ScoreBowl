
class InvalidRoll(Exception):
    """Exception for invalid rolls on a Frame"""
    pass

class FrameComplete(Exception):
    """Exception for action taken on a completed frame."""
    pass

class ScoringComplete(Exception):
    """Exception for attempting to score a frame which has already been scored."""

class StandardFrame(object):
    def __init__(self, max_pins:int=10):
        self.max_pins = max_pins

        self.roll_one = None
        self.roll_two = None

        self.is_strike = False
        self.is_spare = False
        self.is_complete = False

        self.frame_score = None


    def _set_is_strike(self) -> bool:
        """Set the value for the is_strike attribute.  Return the attribute value"""
        self.is_strike = bool(self.roll_one == self.max_pins)

        return self.is_strike

    def _set_is_spare(self) -> bool:
        """Set the value for the is_spare attribute.  Return the attribute value"""
        try:
            self.is_spare = bool((self.roll_one + self.roll_two) == self.max_pins)
        except Exception:
            self.is_spare = False

        return self.is_spare

    def _set_is_complete(self) -> bool:
        """Set the value of the is_complete attribute.  Return the attribute value."""
        self.is_complete = any([self.is_strike, self.is_spare,
                                bool(self.roll_one is not None and self.roll_two is not None)])

        return self.is_complete

    def _is_valid_roll(self, pins:int) -> None:
        """General validation of the roll value passed in.
        Must be a positive integer which is less than the max_pins or zero.
        """
        if not isinstance(pins, int) and self.max_pins >= pins >= 0:
            raise InvalidRoll(f'Pin value must be a positive integer less than or equal to {self.max_pins}')

    def _is_valid_roll_two(self, pins) -> bool:
        """Do additional validation on a value passed for roll_two.
        Cannot have already rolled a strike and sum of pins passed in
        and roll_one cannot be greater than max_pins"""
        return bool(all([self. max_pins >= self.roll_one + pins, self.is_strike is False]))

    def score_roll(self, pins_down:int) -> dict:
        """Add a roll according to state of the objects attributes.  Attempts to set frame total as well
        First method call sets roll_one, second sets roll_two.

        Returns a dictionary of the frames attribute values.
        """
        self._is_valid_roll(pins_down)

        if self.roll_one is None:
            self.roll_one = pins_down
            self._set_is_strike()
        elif self.roll_two is None:
            if self._is_valid_roll_two(pins_down):
                self.roll_two = pins_down
                self._set_is_spare()
            else:
                raise InvalidRoll('Invalid value for 2nd roll')
        else:
            raise InvalidRoll('Frame not eligible for additional rolls')

        # set value and then try to score frame if is complete
        if self._set_is_complete() and self.frame_score is None:
            self.score_frame()

        return self.__dict__

    def score_frame(self, bonus_one:int=None, bonus_two:int=None) -> int or None:
        """Score the frame.  Requires bonus values passed in for strike or spare.
        Returns the frame_score as integer when able to score None if unable to score with data avaialble"""
        # validate any bonus roll value passed in.  Will raise exception if invalid
        [self._is_valid_roll(arg) for arg in [bonus_one, bonus_two] if arg is not None]

        if self.frame_score:
            raise ScoringComplete('Frame already scored.  No alterations possible')

        if all([self.is_strike, bonus_one is not None and bonus_two is not None]):
            self.frame_score = self.roll_one + bonus_one + bonus_two
        elif all([self.is_spare, bonus_one is not None]):  # bonus_two passed will be ignored...
            self.frame_score = self.roll_one + self.roll_two + bonus_one
        elif all([not self.is_strike, not self.is_spare, self.roll_one is not None, self.roll_two is not None]):
            self.frame_score = self.roll_one + self.roll_two

        return self.frame_score


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
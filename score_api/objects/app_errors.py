
class InvalidRoll(Exception):
    """Exception for invalid rolls on a Frame"""
    pass

class FrameComplete(Exception):
    """Exception for action taken on a completed frame."""
    pass

class ScoringComplete(Exception):
    """Exception for attempting to score a frame which has already been scored."""

class GameOver(Exception):
    """Exception for when a game altering actions are attempted on a completed game."""
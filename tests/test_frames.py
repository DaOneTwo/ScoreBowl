from score_api.objects import frames


class TestStandardFrame(object):
    def test_initialization(self):
        """test the initialization of a frame object"""
        f = frames.StandardFrame()
        assert(f.roll_one is None)
        assert(f.roll_two is None)
        assert(f.frame_score is None)
        assert(f.is_strike is False)
        assert(f.is_spare is False)
        assert(f.is_complete is False)
        assert(not hasattr(f, 'roll_three'))

    def test_frame_strike(self):
        """Test adding a first roll which is not a strike."""
        f = frames.StandardFrame()
        roll_value = 10
        f.add_roll(roll_value)
        assert(f.roll_one == roll_value)
        assert(f.roll_two is None)
        assert(f.is_strike is True)
        assert(f.is_spare is False)
        assert(f.frame_score is None)
        assert(f.is_complete is True)
        assert(f.frame_score is None)  # will not be scored until bonus rolls are able to be passed in.

    def test_frame_spare(self):
        """Test a frame which is rolled to be a spare.  Default max pins"""
        f = frames.StandardFrame()
        roll1, roll2 = 8, 2
        # add roll one
        f.add_roll(roll1)
        assert(f.roll_one == roll1)
        assert(f.roll_two is None)
        assert(f.is_strike is False)
        assert(f.is_spare is False)
        assert(f.is_complete is False)
        assert(f.frame_score is None)
        # add our second roll  after this we should have a valid spare
        f.add_roll(roll2)
        assert(f.roll_one == roll1)
        assert(f.roll_two == roll2)
        assert(f.is_strike is False)
        assert(f.is_spare is True)
        assert(f.is_complete is True)
        assert(f.frame_score is None)  # will not be scored until we are able to pass in the bonus score

    def test_frame_regular_joe(self):
        """Test a "normal" frame. Something like your regular joe might roll.  IE not a strike or a spare."""
        f = frames.StandardFrame()
        roll1, roll2 = 5, 2
        f.add_roll(roll1)
        assert (f.roll_one == roll1)
        assert (f.roll_two is None)
        assert (f.is_strike is False)
        assert (f.is_spare is False)
        assert (f.is_complete is False)
        assert (f.frame_score is None)

        f.add_roll(roll2)
        # This tests that the frame got scored properly
        assert (f.roll_one == roll1)
        assert (f.roll_two == roll2)
        assert (f.is_strike is False)
        assert (f.is_spare is False)
        # frame should be complete and scored after adding a second roll which does not create a spare
        assert (f.is_complete is True)
        assert (f.frame_score == roll1 + roll2)

    def test_score_later_strike(self):
        """test coming back to score a strike frame later"""

        f = frames.StandardFrame()
        f.roll_one, f.is_strike = 10, True

        # test unsuccessful scoring do this first because it will leave our object in a state which we can try
        # again
        success, score = f.score_frame(bonus_one=10)  # with only one bonus roll
        assert (all([not success, f.frame_score is None, f.is_complete is True,
                     score == 'Unable to score frame with values provided.']))
        success, score = f.score_frame()  # no bonus rolls
        assert (all([not success, f.frame_score is None, f.is_complete is True,
                     score == 'Unable to score frame with values provided.']))

        # test successful scoring of a strike with 2 non strike/spare rolls (not that it makes a difference.
        success, score = f.score_frame(bonus_one=9, bonus_two=0)
        assert(all([success, f.frame_score == 19 == score, f.is_complete is True]))

        # test successful scoring of a strike with 2 strikes afterwards
        f = frames.StandardFrame()
        f.roll_one, f.is_strike = 10, True
        success, score = f.score_frame(bonus_one=10, bonus_two=10)
        assert (all([success, f.frame_score == 30 == score, f.is_complete is True]))

    def test_score_later_spare(self):
        """test coming back to score a spare frame later"""

        f = frames.StandardFrame()
        f.roll_one, f.roll_two, f.is_strike, f.is_spare = 8, 2, False, True

        # test unsuccessful scoring do this first because it will leave our object in a state which we can try
        # again
        success, score = f.score_frame()  # no bonus rolls
        assert (all([not success, f.frame_score is None, f.is_complete is True,
                     score == 'Unable to score frame with values provided.']))

        # test a successful scoring of a spare
        success, score = f.score_frame(bonus_one=10)
        assert(all([success, f.frame_score == 20 == score, f.is_complete is True]))


class TestFinalFrame(object):
    def test_initialization(self):
        """test the initialization of a frame object"""
        f = frames.FinalFrame()
        assert(all([f.roll_one is None, f.roll_two is None, f.roll_three is None, f.frame_score is None,
                    f.is_strike is False, f.is_spare is False, f.is_complete is False]))

    def test_frame_strike(self):
        """Test adding a first roll which is not a strike."""
        f = frames.FinalFrame()
        roll1 = 10
        f.add_roll(roll1)
        assert(all([f.roll_one == roll1, f.roll_two is None, f.roll_three is None, f.is_strike is True,
                    f.is_spare is False, f.frame_score is None, f.is_complete is False]))
        roll2 = 10
        f.add_roll(roll2)
        assert (all([f.roll_one == roll1, f.roll_two == roll2, f.roll_three is None, f.is_strike is True,
                     f.is_spare is False, f.frame_score is None, f.is_complete is False]))
        roll3 = 10
        f.add_roll(roll3)
        assert (all([f.roll_one == roll1, f.roll_two == roll2, f.roll_three == roll3,
                     f.is_strike is True, f.is_spare is False, f.frame_score == 30,
                     f.is_complete is True]))

    def test_frame_spare(self):
        """Test a frame which is rolled to be a spare"""
        f = frames.FinalFrame()
        roll1, roll2 = 8, 2
        f.add_roll(roll1)
        assert(all([f.roll_one == roll1, f.roll_two is None, f.is_strike is False, f.is_spare is False,
                    f.is_complete is False]))
        f.add_roll(roll2)
        assert (all([f.roll_one == roll1, f.roll_two == roll2, f.is_strike is False, f.is_spare is True,
                     f.is_complete is False]))
        roll3 = 10
        f.add_roll(roll3)
        assert (all([f.roll_one == roll1, f.roll_two == roll2, f.roll_three == roll3,
                     f.is_strike is False, f.is_spare is True, f.frame_score == 20,
                     f.is_complete is True]))

    def test_frame_regular_joe(self):
        """Test a "normal" frame. Something like your regular joe might roll.  IE not a strike or a spare."""
        f = frames.StandardFrame()
        roll1, roll2 = 5, 2
        f.add_roll(roll1)
        assert (all([f.roll_one == roll1, f.roll_two is None, f.is_strike is False, f.is_spare is False,
                     f.is_complete is False]))
        f.add_roll(roll2)
        # This tests that the frame got scored properly
        assert (all([f.roll_one == roll1, f.roll_two == roll2, f.is_strike is False, f.is_spare is False,
                     f.is_complete is True, f.frame_score == roll1 + roll2]))
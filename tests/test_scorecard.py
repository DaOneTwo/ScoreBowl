from score_api.objects.scorecard import GameScorecard


class TestScorecard(object):
    def test_2_spares(self):
        """test rolling 2 spares in a row"""
        card = GameScorecard(max_frames=10)
        roll_value = 5
        for roll in range(1, 5):
            # 4 rolls with value of 5 each time which should be 2 spares
            roll_result = card.add_roll(roll_value)
            if roll == 3:
                assert(all([len(card.frames) == 2,
                            roll_result.get('player_running_score') == 15,
                            card.get_frame(2).roll_two is None]))
                assert(card.get_running_total() == 15)
                frame1 = card.get_frame(1)
                assert(frame1.is_complete is True)
                assert(frame1.roll_one == 5 == frame1.roll_two)
                assert(frame1.is_spare is True)
                assert(frame1.frame_score == 15)
        assert (card.get_running_total() == 15)

    def test_perfect_game(self):
        """test a perfect game"""
        card = GameScorecard()
        roll_count = 1
        frame_index = 1

        game_complete = False
        while not game_complete:
            details = card.add_roll(10)
            print(f'{roll_count} : {frame_index} : {details}\n')
            if details.get('player_game_complete') is True:
                game_complete = True
            else:
                roll_count += 1
                if details.get('advance_player') is True:
                    frame_index += 1

        assert(card.running_total == 300)
        assert(roll_count == 12)


    def test_strike_normal(self):
        # test case 1
        card = GameScorecard(max_frames=10)
        card.add_roll(10)
        card.add_roll(9)
        card.add_roll(0)
        assert(card.get_running_total() == 28)
        f1, f2 = card.get_frame(1), card.get_frame(2)
        assert(f1.frame_score == 19)
        assert(f2.frame_score == 9)

        # test case 2
        card = GameScorecard(max_frames=10)
        card.add_roll(10)
        card.add_roll(7)
        card.add_roll(3)
        assert (card.get_running_total() == 20)
        f1, f2 = card.get_frame(1), card.get_frame(2)
        assert (f1.frame_score == 20)
        assert (f2.frame_score == None)

    def test_regular_game(self):
        card = GameScorecard()
        rolls = [2, 2, 3, 4, 5, 5, 10, 9, 0, 1, 0, 10, 5, 5, 6, 4, 9, 1, 9 ]
        frame_index = 1
        for index, roll in enumerate(rolls, 1):
            print(f'{frame_index} : {index} : {roll}\n')
            roll_details = card.add_roll(roll)
            # check where we should advance player/frame
            if index in [2, 4, 6, 7, 9, 11, 12, 14, 16, 19]:
                assert(roll_details.get('advance_player') is True)
            if index == 2:
                assert(roll_details.get('player_running_score') == 4)
            if index in [4, 5, 6]:
                assert(roll_details.get('player_running_score') == 11)
            if index in [7, 8]:
                assert(roll_details.get('player_running_score') == 31)
            if index in [9, 10]:
                assert(roll_details.get('player_running_score') == 59)
            if index in [11, 12, 13]:
                assert(roll_details.get('player_running_score') == 60)
            if index == 14:
                assert(roll_details.get('player_running_score') == 80)
            if index in [15, 16]:
                assert(roll_details.get('player_running_score') == 96)
            if index in [17, 18]:
                assert(roll_details.get('player_running_score') == 115)
            if index == 19:
                assert(roll_details.get('player_running_score') == 134)
                assert(roll_details.get('player_game_complete') is True)

            if roll_details.get('advance_player') is True:
                frame_index += 1

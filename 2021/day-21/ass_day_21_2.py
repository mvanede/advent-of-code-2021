from utils.lib import get_timer, panswer, pruntime

_ST = get_timer()


class Player():
    def __init__(self, starting_point, score):
        self.score = score
        self.position = starting_point

    def next_turn(self, dice_score):
        self.position = (self.position + dice_score) % 10
        self.score += self.position + 1

    def has_won(self):
        return self.score >= 21

    def get_copy(self):
        return Player(self.position, self.score)


def get_cache_key(player1, player2, turn):
    return "".join([str(x) for x in [player1.score, player1.position, player2.score, player2.position, turn]])


VICTORY_CACHE = {}


def roll(player1, player2, turn=0):
    _cache_key = get_cache_key(player1, player2, turn)
    if _cache_key in VICTORY_CACHE.keys():
        return VICTORY_CACHE[_cache_key]

    _player1_victories = 0
    _player2_victories = 0

    for dice1 in range(1, 4):
        for dice2 in range(1, 4):
            for dice3 in range(1, 4):
                dice_score = dice1 + dice2 + dice3
                _player1 = player1.get_copy()
                _player2 = player2.get_copy()
                if turn == 0:
                    _player1.next_turn(dice_score)
                    if _player1.has_won():
                        _player1_victories += 1
                    else:
                        p1, p2 = roll(_player1.get_copy(), _player2.get_copy(), (turn + 1) % 2)
                        _player1_victories += p1
                        _player2_victories += p2
                else:
                    _player2.next_turn(dice_score)
                    if _player2.has_won():
                        _player2_victories += 1
                    else:
                        p1, p2 = roll(_player1.get_copy(), _player2.get_copy(), (turn + 1) % 2)
                        _player1_victories += p1
                        _player2_victories += p2

    VICTORY_CACHE[_cache_key] = _player1_victories, _player2_victories
    return _player1_victories, _player2_victories

'''
Player 1 starting position: 3
Player 2 starting position: 4
'''
player1_victories, player2_victories = roll(Player(3 - 1, 0), Player(4 - 1, 0))
panswer(player1_victories)
panswer(player2_victories)

pruntime(_ST)
# 193753136998081
from utils.lib import get_timer, panswer, pruntime
_ST = get_timer()


# CODE HERE
class DeterministicDice():
    def __init__(self):
        self.state = 0
        self.roll_count = 0

    def roll(self):
        self.state+=1
        self.roll_count += 1
        return self.state


class Player():
    def __init__(self, dice, starting_point):
        self.score = 0
        self.position = starting_point
        self._dice = dice

    def next_turn(self):
        s = [dice.roll(), dice.roll(), dice.roll()]
        self.position = (self.position + sum(s)) % 10
        self.score += self.position+1


'''
Player 1 starting position: 3
Player 2 starting position: 4
'''
dice = DeterministicDice()
player1 = Player(dice, 3-1)
player2 = Player(dice, 4-1)

while player1.score<1000 and player2.score<1000:
    player1.next_turn()
    if player1.score >= 1000:
        panswer(dice.roll_count * player2.score)
        break

    player2.next_turn()
    if player2.score >= 1000:
        panswer(dice.roll_count * player1.score)
        break

pruntime(_ST)
# 995904
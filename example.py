import sys

sys.path.append('./src')

from sooli import Player, Playground

if __name__ == '__main__':
    p1 = Player()
    p2 = Player()
    while True:
        ground = Playground(p1, p2, 1)
        winner, target, chase = ground()
        if winner == 0:
            print('Game Tied with target = {}, chase = {}'.format(target, chase))
        else:
            print('Player {} won with target = {}, chase = {}'.format(winner, target, chase))
        p1.reset()
        p2.reset()

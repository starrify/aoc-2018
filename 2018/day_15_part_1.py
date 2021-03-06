# coding: utf8

import sys


def main():
    arena = [list(line.strip()) for line in sys.stdin]
    INIT_HP = 200
    ATTACK = 3
    players = [
        (
            (x, y),
            {'pos': (x, y), 'type': grid, 'hp': INIT_HP}
        )
        for x, row in enumerate(arena)
        for y, grid in enumerate(row)
        if grid in 'GE'
    ]
    for _, player in players:
        arena[player['pos'][0]][player['pos'][1]] = player
    rivals = {
        'G': 'E',
        'E': 'G',
    }
    steps = ((-1, 0), (0, -1), (0, 1), (1, 0))
    n_round = 0
    while len(set(x['type'] for _, x in players)) > 1:
        n_round += 1
        players = sorted(players)
        for idx, (_, player) in enumerate(players):
            if player['hp'] <= 0:
                continue
            # target locking
            nearest_target = (float('inf'), None, None)  # dist, target_pos, init_step
            dist_map = [
                [
                    (float('inf'), None)  # dist, init_step
                    for _ in arena[0]
                ]
                for _ in arena
            ]
            active = [(player['pos'], 0, None)]  # pos, dist, init_step
            dist_map[player['pos'][0]][player['pos'][1]] = (0, None)
            while not nearest_target[2] and active:
                new_active = []
                for pos, dist, _init_step in active:
                    for step in steps:
                        init_step = _init_step or step
                        new_pos = tuple(sum(x) for x in zip(pos, step))
                        if dist_map[new_pos[0]][new_pos[1]] > (dist + 1, init_step):
                            dist_map[new_pos[0]][new_pos[1]] = (dist + 1, init_step)
                            if arena[new_pos[0]][new_pos[1]] == '.':
                                new_active.append((new_pos, dist + 1, init_step))
                            elif arena[new_pos[0]][new_pos[1]] == '#':
                                pass
                            elif arena[new_pos[0]][new_pos[1]]['type'] == rivals[player['type']]:
                                nearest_target = min(nearest_target, (dist + 1, new_pos, init_step))
                active = new_active
            # move
            if nearest_target[0] > 1 and nearest_target[2]:
                arena[player['pos'][0]][player['pos'][1]] = '.'
                player['pos'] = tuple(sum(x) for x in zip(player['pos'], nearest_target[2]))
                arena[player['pos'][0]][player['pos'][1]] = player
            # target locking.. yet again
            target = (float('inf'), None, None)  # hp, step, target
            for step in steps:
                new_pos = tuple(sum(x) for x in zip(player['pos'], step))
                if not isinstance(arena[new_pos[0]][new_pos[1]], dict):
                    continue
                tmp_target = arena[new_pos[0]][new_pos[1]]
                if tmp_target['type'] != rivals[player['type']]:
                    continue
                target = min(target, (tmp_target['hp'], step, tmp_target))
            # attack
            if not target[2]:
                continue
            # the previous selected target shall be still optimal after moving
            target = target[2]
            target['hp'] -= ATTACK
            if target['hp'] <= 0:
                arena[target['pos'][0]][target['pos'][1]] = '.'
                if len(set(x['type'] for _, x in players if x['hp'] > 0)) == 1:
                    # last opponent eliminated
                    if any(x['hp'] > 0 for _, x in players[idx + 1:]):
                        # not a complete last round
                        n_round -= 1
        players = [(x['pos'], x) for _, x in players if x['hp'] > 0]
        if False:
            print(n_round)
            print(players)
            for row in arena:
                print(''.join(
                    x if isinstance(x, str) else x['type'] for x in row
                ))
    print(n_round, sum(x['hp'] for _, x in players))
    print(n_round * sum(x['hp'] for _, x in players))


if __name__ == '__main__':
    main()

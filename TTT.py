import numpy as np

# show the position of chess board.
def print_position():
    print('+---+---+---+')
    print('| ' + '1' + ' | ' + '2' + ' | ' + '3' + ' |')
    print('+---+---+---+')
    print('| ' + '4' + ' | ' + '5' + ' | ' + '6' + ' |')
    print('+---+---+---+')
    print('| ' + '7' + ' | ' + '8' + ' | ' + '9' + ' |')
    print('+---+---+---+')


# show the state of chess board.
def print_chess_board(state):
    dic = {1: 'X', -1: 'O', 0: ' '}
    print('+---+---+---+')
    print('| ' + dic[state[0]] + ' | ' + dic[state[1]] + ' | ' + dic[state[2]] + ' |')
    print('+---+---+---+')
    print('| ' + dic[state[3]] + ' | ' + dic[state[4]] + ' | ' + dic[state[5]] + ' |')
    print('+---+---+---+')
    print('| ' + dic[state[6]] + ' | ' + dic[state[7]] + ' | ' + dic[state[8]] + ' |')
    print('+---+---+---+')

# get the reward of state:
# 1: the game end.
# 0: on going
# -1: tie game
def reward(state):
    if state[0] == state[1] == state[2] and state[0] != 0:
        return 1
    elif state[3] == state[4] == state[5] and state[3] != 0:
        return 1
    elif state[6] == state[7] == state[8] and state[6] != 0:
        return 1
    elif state[0] == state[3] == state[6] and state[0] != 0:
        return 1
    elif state[1] == state[4] == state[7] and state[1] != 0:
        return 1
    elif state[2] == state[5] == state[8] and state[2] != 0:
        return 1
    elif state[0] == state[4] == state[8] and state[0] != 0:
        return 1
    elif state[2] == state[4] == state[6] and state[2] != 0:
        return 1

    if 0 in state:
        return 0
    else:
        return -1

# get the all states of chess board.
def get_all_states(cur_state, cur_chess, all_states):
    for i in range(9):
        if cur_state[i] == 0:
            new_state = cur_state[:]
            new_state[i] = cur_chess
            if not tuple(new_state) in all_states.keys():
                all_states[tuple(new_state)] = 0
                if reward(new_state) == 0:
                    get_all_states(new_state, -cur_chess, all_states)


def get_states():
    cur_chess = 1
    cur_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    all_states = {}
    all_states[tuple(cur_state)] = 0
    get_all_states(cur_state, cur_chess, all_states)
    return all_states

# get the random choice of a state
def action(state):
    res = []
    for i in range(9):
        if state[i] == 0:
            res.append(i)
    return res[np.random.randint(0, len(res))]

# get the next step of available states
def next_value(cur_state, all_states, cur_chess):
    if reward(cur_state) == 0:
        res = []
        for i in range(9):
            if cur_state[i] == 0:
                tmp = cur_state[:]
                tmp[i] = cur_chess
                res.append(all_states[tuple(tmp)])
        return res
    else:
        return [0]

# update the value of former states
def feedback_value(cur_state, all_states, pos, step=0.1, rate=0.9):
    pre_state = cur_state[:]
    while len(pos) > 1:
        pre_state[pos[-1]] = 0
        all_states[tuple(pre_state)] = all_states[tuple(pre_state)] + step * (
                rate * all_states[tuple(cur_state)] - all_states[tuple(pre_state)])
        cur_state = pre_state[:]
        pos = pos[:-1]
    return 0

# train the data
def train(epochs=10000, step=0.1, rate=0.9):
    for epoch in range(epochs):
        state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        pos = []
        chess = 1
        while reward(state) == 0:
            p = action(state)
            pos.append(p)
            state[p] = chess
            if reward(state) == 1:
                if chess == 1:
                    all_states[tuple(state)] = 1
                elif chess == -1:
                    all_states[tuple(state)] = -1
                break
            elif chess == 1:
                chess = -1
                v1 = next_value(state, all_states, chess)
                v2 = (rate * min(v1) - all_states[tuple(state)])
                all_states[tuple(state)] += step * v2
            else:
                chess = 1
                v1 = next_value(state, all_states, chess)
                v2 = (rate * max(v1) - all_states[tuple(state)])
                all_states[tuple(state)] += step * v2

        feedback_value(state, all_states, pos)

# get the result with the max value
def choose(state, all_states):
    v = -2
    res = 0
    for i in range(9):
        temp = state[:]
        if state[i] == 0:
            temp[i] = 1
            if all_states[tuple(temp)] > v:
                v = all_states[tuple(temp)]
                res = i
    return res

# play with AI
def play_ai():
    state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    while 1:
        pos_ai = choose(state, all_states)
        state[pos_ai] = 1
        print_chess_board(state)
        if reward(state) == 1:
            print('AI win this game. ')
            break
        elif reward(state) == -1:
            print('It is a tie game.')
            break

        #pos = int(input('Enter the position that you want, please. '))
        while 1:
            pos_input = input('Enter the position that you want, please. ')
            try:
                pos_pl = int(pos_input)
            except:
                print('Please enter a number from 1 to 9.')
                continue
            else:
                if pos_pl > 9 or pos_pl < 1:
                    print('Please enter a number from 1 to 9.')
                    continue
                elif state[pos_pl - 1] != 0:
                    print('The position has been taken. Please enter a empty position.')
                    continue

            state[pos_pl - 1] = -1
            print_chess_board(state)
            break

        if reward(state) == 1:
            print('You win this game. ')
            break

# play with other player
def play_human():
    state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    round = 1
    player = 1
    while 1:
        print_chess_board(state)
        while 1:
            pos_input = input('Player' + str(player) + '. Enter the position that you want, please. ')
            try:
                pos_pl = int(pos_input)
            except:
                print('Please enter a number from 1 to 9.')
                continue
            else:
                if pos_pl > 9 or pos_pl < 1:
                    print('Please enter a number from 0 to 9.')
                    continue
                elif state[pos_pl - 1] != 0:
                    print('The position has been taken. Please enter a empty position.')
                    continue
                else:
                    break

        if player == 1:
            state[pos_pl - 1] = 1
        else:
            state[pos_pl - 1] = -1

        if reward(state) == 1:
            print_chess_board(state)
            print('Player' + str(player) + '. You win this game.')
            break
        elif reward(state) == -1:
            print_chess_board(state)
            print('It is a tie game.')
            break

        player = player % 2 + 1
        round += 1

# main function
if __name__ == "__main__":
    state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    all_states = get_states()
    train()

    print("Here is the position number of chessboard.")
    print_position()
    print("*************")
    while 1:
        mode_input = input("How many players? ")
        try:
            mode = int(mode_input)
        except:
            print('Please enter 1 or 2.')
            continue

        if mode == 2:
            play_human()
        elif mode == 1:
            play_ai()
        else:
            print("Please enter 1 or 2.")
            continue

        print('Do you wanna restart the game? (Y/N)')
        flag = input()
        if flag == 'Y' or flag == 'y':
            continue
        else:
            break

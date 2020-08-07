import numpy as np
def print_position():
    print('+---+---+---+')
    print('| '+'1'+' | '+'2'+' | '+'3'+' |')
    print('+---+---+---+')
    print('| '+'4'+' | '+'5'+' | '+'6'+' |')
    print('+---+---+---+')
    print('| '+'7'+' | '+'8'+' | '+'9'+' |')
    print('+---+---+---+')

def print_chess_board(state):
    dic = {1:'X', -1:'O', 0:' '}
    print('+---+---+---+')
    print('| ' + dic[state[0]] + ' | ' + dic[state[1]] + ' | ' + dic[state[2]] + ' |')
    print('+---+---+---+')
    print('| ' + dic[state[3]] + ' | ' + dic[state[4]] + ' | ' + dic[state[5]] + ' |')
    print('+---+---+---+')
    print('| ' + dic[state[6]] + ' | ' + dic[state[7]] + ' | ' + dic[state[8]] + ' |')
    print('+---+---+---+')

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

def action(state):
    res = []
    for i in range(9):
        if state[i] == 0:
            res.append(i)
    return res[np.random.randint(0,len(res))]

def next_value(state, all_states, chess):
    if reward(state) == 0:
        value = []
        for i in range(9):
            ###
            if state[i] == 0:
                res = state[:]
                res[i] = chess
                value.append(all_states[tuple(res)])
        return value
    else:
        return [0]

def feedback_value(state, all_states, pos, step=0.1, rate=0.9):
    pre_state = state[:]
    while len(pos) > 1:
        pre_state[pos[-1]] = 0
        all_states[tuple(pre_state)] = all_states[tuple(pre_state)] + step*(rate * all_states[tuple(state)] - all_states[tuple(pre_state)])
        state = pre_state[:]
        pos = pos[:-1]
    return 0

def train(epochs = 10000, step=0.1, rate=0.9):
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

def play_ai():
    state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    while 1:
        postion = choose(state, all_states)
        state[postion] = 1
        print_chess_board(state)
        if reward(state) == 1:
            print('AI win.')
            break
        elif reward(state) == -1:
            print('It is a tie game.')
            break
        pos = int(input("Enter the position that you want, please. "))

        if pos > 9 or pos < 1:
            print('Please enter a number from 1 to 9.')
        elif state[pos-1] != 0:
            print('The position has been taken. Please enter a empty position.')

        state[pos-1] = -1
        print_chess_board(state)
        if reward(state) == 1:
            print('You win.')
            break


def play_human():
    state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    round = 1
    player = 1
    while 1:
        print_chess_board(state)
        pos = int(input('Player'+str(player) + '. Enter the position that you want, please.'))
        if pos > 9 or pos < 1:
            print('Please enter a number from 0 to 9.')
            continue
        elif state[pos-1] != 0:
            print('The position has been taken. Please enter a empty position.')
            continue

        if player == 1:
            state[pos-1] = 1
        else:
            state[pos-1] = -1

        if reward(state) == 1:
            print_chess_board(state)
            print('Player' + str(player) + '. You win this game.')
            break
        elif reward(state) == -1:
            print_chess_board(state)
            print('It is a tie game.')
            break

        player = player%2+1
        round+=1

if __name__ == "__main__":
    state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    all_states = get_states()
    train()

    print("Here is the position number of chessboard.")
    print_position()
    print("*************")
    while 1:
        mode = int(input("How many players? "))
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

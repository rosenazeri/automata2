class TuringMachine:
    def __init__(self, states, input_alphabet, tape_alphabet, transitions, initial_state, blank_symbol, final_states):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.blank_symbol = blank_symbol
        self.final_states = final_states
def build_lcs_turing_machine():
    states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q_accept', 'q_reject'}
    input_alphabet = {'a', 'b', '#'}
    tape_alphabet = {'a', 'b', '#', 'X', 'Y', '_'}
    initial_state = 'q0'
    blank_symbol = '_'
    final_states = {'q_accept'}

    transitions = {
        'q0': {
            'a': ('q1', 'X', 'R'),
            'b': ('q1', 'X', 'R'),
            '#': ('q_reject', '#', 'R')
        },
        'q1': {
            'a': ('q1', 'a', 'R'),
            'b': ('q1', 'b', 'R'),
            '#': ('q2', '#', 'R')
        },
        'q2': {
            'a': ('q3', 'Y', 'R'),
            'b': ('q3', 'Y', 'R'),
            'X': ('q6', 'X', 'L'),
            'Y': ('q6', 'Y', 'L'),
            '_': ('q6', '_', 'L')
        },
        'q3': {
            'a': ('q3', 'a', 'R'),
            'b': ('q3', 'b', 'R'),
            'X': ('q4', 'X', 'R'),
            'Y': ('q4', 'Y', 'R'),
            '_': ('q5', '_', 'L')
        },
        'q4': {
            'a': ('q3', 'Y', 'R'),
            'b': ('q3', 'Y', 'R'),
            'X': ('q6', 'X', 'L'),
            'Y': ('q6', 'Y', 'L'),
            '_': ('q6', '_', 'L')
        },
        'q5': {
            'a': ('q5', 'a', 'L'),
            'b': ('q5', 'b', 'L'),
            'X': ('q0', 'X', 'R'),
            'Y': ('q0', 'Y', 'R'),
            '#': ('q6', '#', 'L')
        },
        'q6': {
            'a': ('q6', 'a', 'L'),
            'b': ('q6', 'b', 'L'),
            'X': ('q7', 'X', 'R'),
            'Y': ('q7', 'Y', 'R'),
            '#': ('q6', '#', 'L')
        },
        'q7': {
            'X': ('q7', 'a', 'R'),
            'Y': ('q7', 'b', 'R'),
            '#': ('q_accept', '#', 'R')
        }
    }

    return TuringMachine(states, input_alphabet, tape_alphabet, transitions, initial_state, blank_symbol, final_states)


def find_lcs(str1, str2):
    m = len(str1)
    n = len(str2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    index = dp[m][n]
    lcs = [""] * index

    i, j = m, n
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            lcs[index - 1] = str1[i - 1]
            i -= 1
            j -= 1
            index -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(lcs)

if __name__ == "__main__":
    str1 = input("لطفاً رشته اول را وارد کنید: ")
    str2 = input("لطفاً رشته دوم را وارد کنید: ")
    lcs = find_lcs(str1, str2)
    print(f"بزرگترین زیررشته مشترک بین '{str1}' و '{str2}' است: '{lcs}'")
    tm = build_lcs_turing_machine()

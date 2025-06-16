class NPDA:
    def __init__(self, states, input_alphabet, stack_alphabet, transitions, initial_state, initial_stack_symbol,
                 final_states):
        self.states = states
        self.input_alphabet = input_alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.initial_stack_symbol = initial_stack_symbol
        self.final_states = final_states

    def __str__(self):
        result = []
        result.append("States: " + str(self.states))
        result.append("Input Alphabet: " + str(self.input_alphabet))
        result.append("Stack Alphabet: " + str(self.stack_alphabet))
        result.append("Initial State: " + str(self.initial_state))
        result.append("Initial Stack Symbol: " + str(self.initial_stack_symbol))
        result.append("Final States: " + str(self.final_states))
        result.append("Transitions:")
        for state in self.transitions:
            for input_symbol in self.transitions[state]:
                for stack_top in self.transitions[state][input_symbol]:
                    for transition in self.transitions[state][input_symbol][stack_top]:
                        result.append(f"  δ({state}, {input_symbol}, {stack_top}) -> {transition}")
        return "\n".join(result)

def grammar_to_npda(grammar):
    variables = grammar['variables']
    terminals = grammar['terminals']
    productions = grammar['productions']
    start_symbol = grammar['start_symbol']

    states = set()
    transitions = {}

    state_counter = 0

    def new_state():
        nonlocal state_counter
        state = f"q{state_counter}"
        state_counter += 1
        states.add(state)
        return state

    q_start = new_state()
    q_push_start = new_state()
    q_accept = new_state()

    input_alphabet = terminals
    stack_alphabet = variables.union(terminals).union({'Z'})
    initial_state = q_start
    initial_stack_symbol = 'Z'
    final_states = {q_accept}

    transitions[q_start] = {
        'ε': {('ε', 'Z'): [(q_push_start, [start_symbol, 'Z'])]}
    }

    transitions[q_push_start] = {}

    for variable in variables:
        for production in productions[variable]:
            key = ('ε',)
            if key not in transitions[q_push_start]:
                transitions[q_push_start][key] = {}

            stack_top = (variable,)
            production_reversed = list(production[::-1]) if production != ['ε'] else []

            if stack_top not in transitions[q_push_start][key]:
                transitions[q_push_start][key][stack_top] = []

            transitions[q_push_start][key][stack_top].append((q_push_start, production_reversed))

    for terminal in terminals:
        key = (terminal,)
        transitions[q_push_start][('q_push', terminal)] = {
            (terminal,): [(q_push_start, ['ε'])]
        }

    if ('ε',) not in transitions[q_push_start]:
        transitions[q_push_start][('ε',)] = {}

    transitions[q_push_start][('ε',)][('Z',)] = [(q_accept, ['Z'])]

    return NPDA(states, input_alphabet, stack_alphabet, transitions, initial_state, initial_stack_symbol, final_states)


def get_grammar_from_user():
    print("تعریف گرامر بدون محدودیت")
    variables = set(input("متغیرها: ").replace(" ", "").split(','))
    terminals = set(input("نشانه‌های پایانی: ").replace(" ", "").split(','))
    productions = {}

    print("تولیدها:")
    for var in variables:
        raw = input(f"{var} → ").replace(" ", "")
        raw_prods = raw.split(',')
        prod_list = [list(prod) if prod != 'ε' else ['ε'] for prod in raw_prods]
        productions[var] = prod_list

    start_symbol = input("نماد آغازین: ").strip()
    return {
        'variables': variables,
        'terminals': terminals,
        'productions': productions,
        'start_symbol': start_symbol
    }

grammar = get_grammar_from_user()
npda = grammar_to_npda(grammar)
print("\nNPDA ساخته شد:\n")
print(npda)

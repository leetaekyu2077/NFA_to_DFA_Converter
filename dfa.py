class DFA:
    def __init__(self):
        self.states = set()
        self.input_symbols = []
        self.start_state = ''
        self.final_states = set()
        self.mapping_function = []
        self.q = []

    def convert_to_dfa(self, nfa):
        self.input_symbols = nfa.input_symbols
        self.start_state = nfa.start_state

        # accessible state만 가지고 states, mapping function, final states 재정의
        self.q.append(nfa.mapping_function[0][0]) # 가장 처음에 시작상태를 큐에 넣음
        self.states.add(nfa.mapping_function[0][0]) # dfa의 상태집합에 시작상태를 추가

        while len(self.q) > 0:
            current = self.q.pop(0)  # 현재 보고 있는 상태 (상태 리스트)
            for i in self.input_symbols:  # 현재 보고 있는 상태를 시작상태로 하는 상태 전이 함수를 새로 정의하여 dfa의 상태전이함수 집합에 추가
                new_mapping_function = (self.make_new_mapping(nfa, current, i))
                if len(new_mapping_function[2]) > 0:  # 새로 정의된 상태 전이 함수에서 결과 상태가 공집합이 아닐 때만 추가
                    self.mapping_function.append(new_mapping_function)
                new_state = ''.join(list(new_mapping_function[2]))
                if (new_state in self.states) is False:  # 한번도 등장하지 않은 새로운 상태일 때
                    self.states.add(new_state)  # 상태 집합에는 하나로 합친 스트링 형태로 추가
                    self.q.append(list(new_mapping_function[2]))  # 큐에는 각 상태가 나열된 리스트 형태로 추가
                    if len(new_mapping_function[2] & nfa.final_states) > 0:
                        self.final_states.add(new_state)

        print(self.states)
        print(self.input_symbols)
        print(self.start_state)
        print(self.final_states)
        for i in self.mapping_function:
            print(i)

    def make_new_mapping(self, nfa, current, input_symbol):
        new_result_state = set()
        for i in range(len(current)):
            for element in nfa.mapping_function:
                if element[0] == current[i] and element[1] == input_symbol:   # 새로운 state의 상태 전이 결과 집합을 구성
                    new_result_state.update(element[2])

        new_mapping_function = (current, input_symbol, new_result_state)
        return new_mapping_function
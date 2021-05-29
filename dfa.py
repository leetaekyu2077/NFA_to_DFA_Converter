class DFA:
    def __init__(self):
        self.states = []
        self.input_symbols = []
        self.start_state = ''
        self.final_states = []
        self.mapping_function = []
        self.q = []  # 새로 나오는 accessible state 를 담아놓을 큐

    def convert_to_dfa(self, nfa):
        self.input_symbols = nfa.input_symbols  # 입력 심볼 그대로
        self.start_state = nfa.start_state  # 시작 상태 그대로

        # accessible state만 가지고 states, mapping function, final states 재정의
        self.q.append(nfa.mapping_function[0][0]) # 가장 처음에 시작상태를 큐에 넣음
        self.states.append(nfa.mapping_function[0][0]) # dfa의 상태집합에 시작상태를 추가

        while len(self.q) > 0:
            current = self.q.pop(0)  # 현재 보고 있는 상태 (상태 리스트)
            for i in self.input_symbols:  # 현재 보고 있는 상태를 시작상태로 하는 상태 전이 함수를 새로 정의하여 dfa의 상태전이함수 집합에 추가
                current = ''.join(current)
                new_mapping_function = (self.make_new_mapping(nfa, current, i))
                if len(new_mapping_function[2]) > 0:  # 새로 정의된 상태 전이 함수의 결과 상태 집합이 공집합이 아닐 때만 추가
                    self.mapping_function.append(new_mapping_function)
                new_state = ''.join(list(new_mapping_function[2]))
                if (new_state in set(self.states)) is False:  # 한번도 등장하지 않은 새로운 상태일 때
                    self.states.append(new_state)  # 상태 집합에는 하나로 합친 스트링을 추가
                    self.q.append(sorted(list(new_mapping_function[2])))  # 큐에는 각 상태들이 정렬된 하나의 리스트를 추가
                    if len(set(list(new_mapping_function[2])) & nfa.final_states) > 0:
                        self.final_states.append(new_state)

        # print("\n<<DFA>>")
        # print("상태 집합 : ", self.states)
        # print("입력 심볼 : ", self.input_symbols)
        # print("시작 상태 : ", self.start_state)
        # print("종결 상태 집합 : ", self.final_states)
        # print("상태 전이 함수")
        # for i in self.mapping_function:
        #     print(i)

    def make_new_mapping(self, nfa, current, input_symbol):
        new_result_state_set = set()
        new_result_state = ''
        for i in range(len(current)):
            for element in nfa.mapping_function:
                if element[0] == current[i] and element[1] == input_symbol:   # 새로운 state의 상태 전이 결과 집합을 구성
                    new_result_state_set.update(element[2])
                    new_result_state = ''.join(sorted(list(new_result_state_set)))

        new_mapping_function = (current, input_symbol, new_result_state)
        return new_mapping_function

    def minimization(self):
        groups = []
        group_num = len(groups)
        groups.append(sorted(list(self.final_states)))  # 종결 상태 집합
        groups.append(sorted(list(set(self.states).difference(self.final_states)))) # 종결 상태 집합 외의 집합

        groups_mapping_function = []
        while len(groups) > group_num:  # partition이 발생했으면 반복
            group_num = len(groups)
            groups_mapping_function = []  # [0] = 입력 심볼, [1] = 상태 그룹, [2] = 그룹 내 상태 인덱스, [3] = 결과 상태 그룹 인덱스
            for i in range(len(self.input_symbols)):  # 각 입력 심볼에 대하여
                for j in range(len(groups)):  # 각 그룹 안에서
                    for k in range(len(groups[j])):  # 그 그룹의 각 상태에 대하여
                        # 해당 상태가 input_symbol을 보고 가는 결과 상태가 어떤 그룹에 속하는가
                        group_index = self.find_which_group(groups[j][k], self.input_symbols[i], groups)
                        # new_mapping_function -> [0] = 입력 심볼, [1] = 상태 그룹, [2] = 그룹 내 상태 인덱스, [3] = 결과 상태 그룹 인덱스
                        new_mapping_function = (i, j, k, group_index)
                        groups_mapping_function.append(new_mapping_function)
            temp = self.partition(groups_mapping_function, groups)
            if temp is not None:
                groups = temp

        # reduced DFA 재정의
        self.states = []
        for state in groups:
            self.states.append('/'.join(state))
        temp_final_state = self.final_states  # 종결 상태 집합 재정의
        self.final_states = []
        for state in groups:
            if len(set(state) & set(temp_final_state)) > 0:
                self.final_states.append('/'.join(state))
        # 상태 전이 함수 재정의
        self.mapping_function = []
        for i in range(len(groups_mapping_function)):
            self.mapping_function.append(('/'.join(groups[groups_mapping_function[i][1]]),  # 상태
                                          self.input_symbols[groups_mapping_function[i][0]],  # 입력 심볼
                                          '/'.join(groups[groups_mapping_function[i][3]])))  # 결과 상태
        self.mapping_function.sort()

    def find_which_group(self, state, input_symbol, groups): # 해당 상태가 input_symbol을 보고 가는 결과 상태가 어떤 그룹에 속하는가
        result = ''
        for each in self.mapping_function:
            if each[0] == state and each[1] == input_symbol: # 해당 상태, 해당 입력 심볼을 가지는 상태 전이 함수
                result = each[2] # string

        if len(result) == 0:  # 해당하는 상태 전이 함수가 없을 때
            print("비정상 종료")
            exit(0)

        for i in range(len(groups)):
            if (result in set(groups[i])) is True:
                return i

    def partition(self, groups_mapping_function, groups):
        for i in range(len(self.input_symbols)):  # 입력 심볼에 대하여
            new_groups = []
            for j in range(len(groups)):  # 한 그룹에 대하여
                result = []
                for k in range(len(groups_mapping_function)):  # 같은 입력 심볼과 같은 그룹에 대한 것들을 찾음
                    if groups_mapping_function[k][0] == i and groups_mapping_function[k][1] == j:
                        # result[0] = 그룹 번호, result[1] = 그룹 내의 상태 번호, result[2] = 결과 상태가 속한 그룹의 번호
                        result.append((groups_mapping_function[k][1],
                                       groups_mapping_function[k][2],
                                       groups_mapping_function[k][3]))
                result_state = result[0][2]  # 첫 번째 결과 상태가 속한 그룹의 번호
                flag = False
                # 같은 입력 심볼에 대하여 한 그룹 안에서 각 상태의 결과 상태 그룹의 번호가 서로 다른 게 있는 지 확인
                for x in range(1, len(result)):
                    if result[x][2] != result_state:
                        flag = True
                        break

                temp_group = []
                if flag is True:  # 서로 다른 게 있다 (=partition 해야한다)
                    for y in range(len(groups)):  # 모든 각 그룹에 대하여
                        temp_group = []
                        for z in range(len(result)):
                            if result[z][2] == y:  # 결과 상태 그룹의 번호가 같은 것들끼리 묶음
                                temp_group.append(groups[result[z][0]][result[z][1]])
                        if len(temp_group) > 0:
                            new_groups.append(temp_group)
                else:
                    for a in range(len(result)):
                        temp_group.append(groups[result[a][0]][result[a][1]])
                    new_groups.append(temp_group)

            if flag is True:
                return new_groups

    def print(self):
        print("\n<<Reduced DFA>>")
        print("상태 집합 : ", self.states)
        print("입력 심볼 : ", self.input_symbols)
        print("시작 상태 : ", self.start_state)
        print("종결 상태 집합 : ", self.final_states)
        print("상태 전이 함수")
        for i in self.mapping_function:
            print(i)
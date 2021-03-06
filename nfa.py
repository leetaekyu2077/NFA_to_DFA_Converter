class NFA:
    def __init__(self, file):
        self.states = set()
        self.input_symbols = []
        self.start_state = ''
        self.final_states = set()
        self.mapping_function = []

        self.states = set(file[0].rstrip("\n").split(" "))  # 상태 집합 구성
        self.input_symbols = file[1].rstrip("\n").split(" ")  # 입력 심볼 집합 구성
        self.start_state = file[2].rstrip("\n")  # 시작 상태
        self.final_states = set(file[3].rstrip("\n").split(" "))  # 종료 상태 집합 구성

        # 상태 전이 함수 구성
        function_line = ""
        state = ""
        symbol = ""
        result = {}
        each_function = ()
        for i in range(4, len(file)):
            function_line = file[i].rstrip("\n").split(" ")
            state = function_line.pop(0)
            symbol = function_line.pop(0)
            result = set(function_line)
            each_function = (state, symbol, result)
            self.mapping_function.append(each_function)






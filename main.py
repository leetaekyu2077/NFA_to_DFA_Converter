from nfa import NFA
from dfa import DFA

filename = input('NFA 파일 이름 입력 : ')
file = open(filename+'.txt', 'r')
read_file = file.readlines()

nfa = NFA(read_file)
dfa = DFA()

dfa.convert_to_dfa(nfa)
dfa.minimization()

print("<<Reduced DFA>>")
dfa.print()

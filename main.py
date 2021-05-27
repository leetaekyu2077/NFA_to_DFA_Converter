import sys
from converter import *

filename = input('NFA 파일 이름 입력 : ')
file = open(filename+'.txt', 'r')
read_file = file.readlines()

nfa = NFA(read_file)


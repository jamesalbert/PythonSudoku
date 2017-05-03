import os
import re
from glob import glob
from itertools import product
from subprocess import PIPE, Popen

con = ['ACP', 'FC']
nak = ['NKP', 'NKT']
var = ['MRV', 'DH']
lcv = ['LCV']
algs = [con, var, nak, lcv]
easy = glob('ExampleSudokuFiles/PE*')[:5]
med = glob('ExampleSudokuFiles/PM*')[:5]
hard = glob('ExampleSudokuFiles/PH*')[:5]

puzzles = list()
puzzles.extend(easy)
puzzles.extend(med)
puzzles.extend(hard)

sols = dict()
print(len(list(product(*algs))))
print(list(product(*algs))[0])
for i, tokens in enumerate(list(product(*algs))):
    print("===========================================")
    print("= {0} =".format(' '.join(tokens)))
    for j, puzzle in enumerate(puzzles):
        command = 'python main.py {0} output/{1}_{2}_{3} 66600 LCV NKP NKT {4}'.format(
            puzzle, i, j, '_'.join(tokens), ' '.join(tokens)
        )
        proc = Popen(command.split(' '), stdout=PIPE)
        ret, _ = proc.communicate()
        times = re.findall('SOLUTION_TIME=(\d+\.\d+)', str(ret))
        bts = re.findall('COUNT_DEADENDS=(\d+)', str(ret))
        nodes = re.findall('COUNT_NODES=(\d+)', str(ret))
        sols['_'.join(tokens)] = sols.get('_'.join(tokens)) or dict()
        sols['_'.join(tokens)]['time'] = sols['_'.join(
            tokens)].get('time') or 0
        sols['_'.join(tokens)]['backtracks'] = sols['_'.join(
            tokens)].get('backtracks') or 0
        sols['_'.join(tokens)]['nodes'] = sols['_'.join(
            tokens)].get('nodes') or 0
        sols['_'.join(tokens)]['time'] += float(times[0])
        sols['_'.join(tokens)]['backtracks'] += float(bts[0])
        sols['_'.join(tokens)]['nodes'] += float(nodes[0])

    print("===========================================")

print(sols)
print('min time: {0}'.format(min(sols, key=lambda x: sols[x]['time'])))
print('min backtracks: {0}'.format(
    min(sols, key=lambda x: sols[x]['backtracks'])))
print('min nodes: {0}'.format(min(sols, key=lambda x: sols[x]['nodes'])))

print('max time: {0}'.format(max(sols, key=lambda x: sols[x]['time'])))
print('max backtracks: {0}'.format(
    max(sols, key=lambda x: sols[x]['backtracks'])))
print('max nodes: {0}'.format(max(sols, key=lambda x: sols[x]['nodes'])))

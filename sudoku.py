import argparse

from pysat.formula import CNF
from pysat.solvers import Solver



def encode(i, j , k, isTrue=False):
    ret = 81*i + 9*j + k
    if isTrue:
        return ret
    return -(ret)

def decode(x):
    x = x-1
    i = x // 81
    j = (x%81) // 9
    k = (x%81)%9  + 1
    return (i , j, k)

def gen_clause():
    clause = CNF()
    # all cell should at least one number from 1 to 9
    for i in range(9):
        for j in range(9):
            disjunction = []
            for k in range(1, 10):
                disjunction.append(encode(i ,j , k, True))
            clause.append(disjunction)
    # ROW cannot appear a repeated number
    for i in range(9):
        for k in range(1,10):
            for j in range(8):
                for jj in range(j+1, 9):
                    clause.append([encode(i,j,k), encode(i,jj,k)])
    
    # COL canoot appear a repeated number

    for j in range(9):
        for k in range(1, 10):
            for i in range(8):
                for ii in range(i+1, 9):
                    clause.append([encode(i,j,k), encode(ii, j, k)])

    # GRID RULE
    for k in range(1,10):
        for ig in range(3):
            for jg in range(3):
                for i in range(3):
                    for j in range(2):
                        for jj in range(j+1, 3):
                            clause.append([encode(3*ig+i, 3*jg+j, k), encode(3*ig+i, 3*jg+jj, k)])
    for k in range(1,10):
        for ig in range(3):
            for jg in range(3):
                for i in range(2):
                    for j in range(3):
                        for ii in range(i+1, 3):
                            for jj in range(3):
                                clause.append([encode(3*ig+i, 3*jg+j, k), encode(3*ig +ii, 3*jg+jj, k)])
    return clause


def solve(clause):
    solver = Solver(bootstrap_with=clause)
    solver.solve()
    print_solution(solver.get_model())

def print_solution(model):
    index = 0
    for sol in model:
        if sol > 0:
            i, j, k = decode(sol)
            index += 1
            if index < 9:
                print(k , end = ' ' )
            else:
                print(k)
                index = 0


def print_to_file(fname, clause):
    print("p cnf {} {}".format(9*9*9, len(clause)))
    for line in clause:
        print( str(line).replace(',' ,'').replace('[', '').replace(']', '')) 



def read_file(fname, clause):
    with open(fname, 'r') as f:
        a = f.read().replace('\n',' ') 
        a = a.split(' ')
        index = 0
        for txt in a:
            if txt == '_' or txt == '':
                index += 1            
            else:               
                k = int(txt)
                i = index // 9
                j = index % 9 
                clause.append([encode(i, j , k , True)])                
                index += 1

def main():
    argp = argparse.ArgumentParser(
        description='Solve Sudoku problems with a SAT solver.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argp.add_argument('--file', type=str,
                      help='the Sudoku question filef')
    argp.add_argument('--all_solutions', action='store_true',
                      help='enumerate all solutions')
    args = argp.parse_args()
    fname = args.file
    clause = gen_clause()
    read_file(fname, clause)
    solve(clause)

if __name__ == "__main__":
    main()


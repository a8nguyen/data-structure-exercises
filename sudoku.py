# -*- coding: utf-8 -*-
"""sudoku.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17Ikt2onrcsIt8dYw86NeruggR2NofnTf
"""

sudoku = [[5, 3, None, None, 7, None, None, None, None],
         [6, None, None, 1, 9, 5, None, None, None],
         [None, 9, 8, None, None, None, None, 6, None],
         [8, None, None, None, 6, None, None, None, 3],
         [4, None, None, 8, None, 3, None, None, 1],
         [7, None, None, None, 2, None, None, None, 6],
         [None, 6, None, None, None, None, 2, 8, None],
         [None, None, None, 4, 1, 9, None, None, 5],
         [None, None, None, None, 8, None, None, 7, 9]]
anotherone = """53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79"""


def translate(puzzle):
    ultimate_list = [[int(x) if x != '.' else None for x in line] for line in puzzle.split()]
    return ultimate_list


def show(puzzle):
  L = [['.' if x == None else str(x) for x in line] for line in puzzle]
  divider = '-+-'.join(['-'*(2*3-1)]*3)
  P=[]
  
  for i in range (3):
    P = P + [' | '.join([' '.join(L[3*i+j][3*k:3*(k+1)]) for k in range(3)]) for j in range(3)] + [divider]
  return '\n'.join(P[:-1])
print show(sudoku)


def fill(puzzle, i, j, v):
  L = [x[:] for x in puzzle]
  L[i][j] = v
  return L


def possible(puzzle, i, j):
  L = [[0 if x == None else int(x) for x in line] for line in puzzle]
  A = set(range(1,9+1))
  #max_sum = (9*9 +9)/(2*3)
  
  row = set(L[i])
  column = set(L[k][j] for k in range (9-1))
  box = [el[(j/3)*3:(j/3+1)*3] for el in L[(i/3)*3:(i/3+1)*3]]
  box_set = set([y for x in box for y in x])
  #if sum(box[i%3]) > max_sum or sum([b[j%3] for b in box]) > max_sum:
    #poss = set()
  #else:
  poss = (A-row-column-box_set if L[i][j] == 0 else set([L[i][j]]))
  return poss

def valid(puzzle):
  L = [[0 if x == None else int(x) for x in line] for line in puzzle]
  column = [[x[t] for x in L] for t in range(9)]
  box = [el[i:i+3] for i in range (0,7,3) for el in L]
  box = [x for f in box for x in f]
  box = [box[i:i+9] for i in range(0,81,9)]
  
  check = map(lambda x: len(set(x)) == 9, L and column and box)
  if False in check:
    return False
  else:
    return True

def solve(puzzle):
  L = puzzle

  empty = [(i,j) for i in xrange(9) for j in xrange(9) if L[i][j] == None]
  index = 0
  while index < 3:
    print index
    i, j = empty[index]
    poss = possible(L, i, j)
    print poss
    if len(poss) == 0: 
      i, j = empty[index-1]
    else:
      for x in poss:
        L = fill(L, i, j, x)
        poss.pop()
        print 
        print show(L)
        break
    
      #L[i][j] == None
    #print L
solve(sudoku)
print range
print range(1,8)
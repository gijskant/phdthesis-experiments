#! /usr/bin/env python
# :noTabs=true:
# (c) Copyright (c) 2017  Gijs Kant
# (c) This file is distributed under the Apache Software License, Version 2.0
# (c) (https://www.apache.org/licenses/LICENSE-2.0.txt).
"""
connectfour.py

Brief: Generates SMV files representing the Connect Four game.

Author: Gijs Kant <gijskant@protonmail.com>

"""
import re
import sys

N = 7 # width of the board
M = 6 # height of the board
K = 4 # number of pieces needed to win

if len(sys.argv) > 1:
  N = int(sys.argv[1])
  if len(sys.argv) > 2:
    M = int(sys.argv[2])
if N < K or M < 1:
  print "Usage: connectfour [N [M]] (for N >= {K}, M >= 1)".format(K)
  sys.exit()

smv_template = '''-- Connect Four {N} x {M}

MODULE main
  VAR
    player     : {{Yellow, Red}};
    board      : array 1..{N} of array 1..{M} of {{None, Yellow, Red}};

  DEFINE
    yellowwins :=
      {yellowwins}
    redwins :=
      {redwins}

  SPEC
    {spec}

  INIT
    {init}

  TRANS
    {trans}
'''

yellowwins = ""
redwins = ""
if N >= K:
  yellowwins += "-- Horizontal\n        "
  redwins += "-- Horizontal\n        "
  for j in range(1, M+1):
    for i in range(1, N+2-K):
      yellowwins += "("
      redwins += "("
      for x in range(0, K):
        yellowwins += "board[{}][{}] = Yellow & ".format(i+x, j)
        redwins += "board[{}][{}] = Red & ".format(i+x, j)
      yellowwins += "TRUE )\n      | "
      redwins += "TRUE )\n      | "
if M >= K:
  yellowwins += "\n      -- Vertical\n        "
  redwins += "\n      -- Vertical\n        "
  for i in range(1, N+1):
    for j in range(1, M+2-K):
      yellowwins += "("
      redwins += "("
      for x in range(0, K):
        yellowwins += "board[{}][{}] = Yellow & ".format(i, j+x)
        redwins += "board[{}][{}] = Red & ".format(i, j+x)
      yellowwins += "TRUE )\n      | "
      redwins += "TRUE )\n      | "
if N >= K and M >= K:
  yellowwins += "\n      -- Diagonal\n        "
  redwins += "\n      -- Diagonal\n        "
  for i in range(1, N+2-K):
    for j in range(1, M+2-K):
      yellowwins += "("
      redwins += "("
      for x in range(0, K):
        yellowwins += "board[{}][{}] = Yellow & ".format(i+x, j+x)
        redwins += "board[{}][{}] = Red & ".format(i+x, j+x)
      yellowwins += "TRUE )\n      | "
      redwins += "TRUE )\n      | "
  for i in range(1, N+2-K):
    for j in range(1, M+2-K):
      yellowwins += "("
      redwins += "("
      for x in range(0, K):
        yellowwins += "board[{}][{}] = Yellow & ".format(N+1-i-x, j+x)
        redwins += "board[{}][{}] = Red & ".format(N+1-i-x, j+x)
      yellowwins += "TRUE )\n      | "
      redwins += "TRUE )\n      | "

yellowwins += "FALSE;"
redwins += "FALSE;"

spec = '''AG !(redwins & yellowwins)
  SPEC
    '''
k = (N*M/2)+1
for i in range(1, k+1):
  spec += "EX (yellowwins"
  if i < k:
    spec += " | AX (!redwins & "
for i in range(1, k+1):
  if i < k:
    spec += ") "
  spec += ") "
spec += '''
  SPEC
    '''
for i in range(1, k+1):
  spec += "EX (redwins"
  if i < k:
    spec += " | AX (!yellowwins & "
for i in range(1, k+1):
  if i < k:
    spec += ") "
  spec += ") "

init = '''player = Yellow &
'''
for i in range(1, N+1):
  for j in range(1, M+1):
    init += "    board[{}][{}] = None &\n".format(i, j)
init += "    TRUE"

trans = "(\n"
#trans = '''!yellowwins & !redwins &
#    next(player) = case player = Yellow : Red;
#                        TRUE : Yellow;
#                   esac &
#    (
#'''
for i in range(1, N+1):
  trans += '''      (
        !yellowwins & !redwins &
        next(player) = case player = Yellow : Red;
                            TRUE : Yellow;
                       esac &
        (board[{}][{}] = None) &
        (
'''.format(i, M)
#  trans += "      ( (board[{}][{}] = None) & \n        (\n".format(i, M)
  for j in range(1, M+1):
    trans += "          next(board[{}][{}]) = case ".format(i, j)
    if (j > 1):
      for k in range(1,j):
        trans += "board[{}][{}] != None & ".format(i, k)
    trans += "board[{}][{}] = None\n".format(i, j)
    trans += '''                                        : player;
                                   TRUE : board[{}][{}];
                              esac &
'''.format(i, j)
  for x in range(1, N+1):
    if x != i:
      for y in range(1, M+1):
        trans += "          next(board[{}][{}]) = board[{}][{}] &\n".format(x, y, x, y)
  trans += "          TRUE \n        )\n      ) | \n"

trans += "      ( (yellowwins | redwins | ("
for i in range(1, N+1):
  trans += "board[{}][{}] != None & ".format(i, M)
trans += "TRUE) ) & \n        (\n"
for x in range(1, N+1):
    for y in range(1, M+1):
      trans += "          next(board[{}][{}]) = board[{}][{}] &\n".format(x, y, x, y)
trans += "          TRUE \n        )\n      )\n    )"

arguments = {'N': N,
             'M': M,
             'yellowwins': yellowwins,
             'redwins': redwins,
             'spec': spec,
             'init': init,
             'trans': trans
            }
smv = smv_template.format(**arguments)
print smv

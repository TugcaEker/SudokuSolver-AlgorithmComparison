#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 05:30:04 2017

@author: mcelik
"""

def same_row(i,j):
    return i[0] == j[0]
def same_col(i,j):
    return i[1] == j[1]
def same_block(i,j):
    return (int(i[0]/3) == int(j[0]/3)) and (int(i[1]/3) == int(j[1]/3))

def get_row_set(i): return [(x , y) for x in range(9) for y in range(9) if same_row((x,y),i)]
def get_col_set(i): return [(x , y) for x in range(9) for y in range(9) if same_col((x,y),i)]
def get_block_set(i): return [(x , y) for x in range(9) for y in range(9) if same_block((x,y),i)]
def get_all_set(i): return [(x , y) for x in range(9) for y in range(9) if (same_row((x,y),i) or same_col((x,y),i) or same_block((x,y),i)) and (x,y) != i]

def empty_state():
    state = dict()
    cs = "123456789"
    for i in range(81):
        state[int(i/9),int(i%9)] = cs
    return state


def gen_state_from_str(su_str):
    state = dict()
    cs = "123456789"
    for i,s in enumerate(su_str):
        if s in cs:
            state[int(i/9),int(i%9)] = s
        else:
            state[int(i/9),int(i%9)] = cs
    return state



def print_grid(state):
    width = 1 + max(len(x) for x in state.values())
    line = "+" + "+".join(['-'*(width*3)]*3) + "+"
    print(line)
    for r in range(9):
        print("|" + "".join(state[r,c].center(width)+('|' if c%3 == 2 else '') for c in range(9)))
        if r%3 == 2:
            print(line)
    print


def get_puzzles_from_file(fname):
    with open(fname) as f:
        lines = f.readlines()
    puzzles = [l.strip() for l in lines]
    return puzzles


def gen_valid_choices(c,state):
    knb = set([state[x] for x in get_block_set(c) if len(state[x]) == 1])
    knr = set([state[x] for x in get_row_set(c) if len(state[x]) == 1])
    knc = set([state[x] for x in get_col_set(c) if len(state[x]) == 1])
    print("".join(set("123456789")-knb.union(knc).union(knr)))

def gen_block_prob(c, state):
    knb = set([state[x] for x in get_block_set(c) if x != c])
    return set(state[c]) - set("".join(knb))


def gen_row_prob(c, state):
    knb = set([state[x] for x in get_row_set(c) if x != c])
    return set(state[c]) - set("".join(knb))


def gen_col_prob(c, state):
    knb = set([state[x] for x in get_col_set(c) if x != c])
    return set(state[c]) - set("".join(knb))


def hasGap(state):
    for i in range(9):
        for j in range(9):
            if len(state[i,j]) == 0:
                return True
    return False

def isCompleted(state):
    for i in range(9):
        for j in range(9):
            if len(state[i,j]) != 1:
                return False
    return True


def totalPossibility(state):
    pos = 1
    for i in range(9):
        for j in range(9):
            pos = pos * len(state[i,j])
    return pos

def getIJ(i):
    return (int(i/9),int(i%9))
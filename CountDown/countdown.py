import unittest
import sys
import numpy as np
"""
Return a list of number that is 1 large number from a list of 25, 50, 100 and 5 small numbers
and a target number that is between 100 and 999
"""

def generate_rand_num():
    large = [np.random.randint(1,5) * 25]
    small = list(np.random.random_integers(10,size = 5))
    target = np.random.randint(100, 1000)
    source = large + small
    return target, source

_operators = ['+','-','*','/']

class IllegalOpError(Exception):
    pass

def eval_op(op, v1, v2):
    assert op in _operators
    if op is '+': value = v1+v2
    if op is '-': value = v1-v2
    if op is '*': value = v1*v2
    if op is '/':
        if v2==0: raise IllegalOpError("Divide by zero")
        if v1%v2>0: raise IllegalOpError("Not divisible")
        value = v1/v2
    if value<0: raise IllegalOpError("Negative result")
    return value

def iter_pairs(L):
    L = sorted(L, reverse=True)
    pair_list = [(L[i], L[j]) for i in xrange(len(L)) for j in xrange(i+1, len(L))]
    return pair_list

def quality(target, value, expression):
    if value is None: return sys.maxint, sys.maxint
    return (abs(target-value), len(expression))

def find_expression(target, source):
    def _find_recursive(values, expressions):
        if len(values)==1:
            return values[0], expressions[0]
        closest = None
        best_expr = None
        for i,j in iter_pairs(range(len(values))):
            for op in _operators:
                #Combining pairs
                try:
                    nv = eval_op(op,values[i],values[j])
                    ne = "(%s %s %s)" % (expressions[i], op, expressions[j])
                    if quality(target,nv,ne) < quality(target, closest, best_expr): closest, best_expr = nv, ne
                    # Pass new source list to
                    nvals = [v for k,v in enumerate(values) if k not in (i,j)] + [nv]
                    nexpr = [v for k,v in enumerate(expressions) if k not in (i,j)] + [ne]
                    nv, ne = _find_recursive(nvals, nexpr)

                    # Check to see if the result is better than the best so far, replace closest and best_expr
                    if quality(target,nv,ne) < quality(target, closest, best_expr): closest, best_expr = nv, ne
                except:
                    pass
        return closest, best_expr

    return _find_recursive(source, [str(v) for v in source])

class Test_Countdown(unittest.TestCase):
    def test_eval_op(self):
        self.assertEquals(eval_op('+', 8, 2), 10)
        self.assertEquals(eval_op('-', 8, 2), 6)
        self.assertEquals(eval_op('*', 8, 2), 16)
        self.assertEquals(eval_op('/', 8, 2), 4)

        try:
            eval_op('/', 8, 0)
        except IllegalOpError:
            pass
        else:
            raise AssertionError("Expected IllegalOpError on divide by zero")

        try:
            eval_op('/', 8, 3)
        except IllegalOpError:
            pass
        else:
            raise AssertionError("Expected IllegalOpError when not divisible")

        try:
            eval_op('-', 3, 8)
        except IllegalOpError:
            pass
        else:
            raise AssertionError("Expected IllegalOpError when result is negative")

    def test_iter_pairs(self):
        self.assertEquals(list(iter_pairs([1,3,5,7,9])), [(9,7), (9,5), (9,3), (9,1), (7,5), (7,3), (7,1), (5,3), (5,1), (3,1)])

    def test_find_expression(self):
        val, ex = find_expression(900, (25,1,2,3,4,5))
        print val, ex
        self.assertEquals(val, 900)
        self.assertEquals(eval(ex), 900)
        val, ex = find_expression(125, (2,4,8,5,25))
        print val, ex
        ops = sum(1 for c in ex if c in _operators)
        self.assertEquals(val, 125)
        self.assertEquals(eval(ex), 125)
        self.assertEquals(ops, 1)

unittest.main(argv=['first-arg-is-ignored'], exit = False)

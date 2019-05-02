import unittest
import time
import numpy as np

"""
Return a list of divisors
"""
def divisors(x):
  n = int(np.floor(np.sqrt(float(x))))
  L = [1]
  for i in xrange(2,n+1):
    if x%i==0:
      L.append(i)
      if i!=x/i:
        L.append(x/i)
  return sorted(L)


"""
  Return True if the number is  semiperfect.
  
"""
def semiperfect(n):
  div = divisors(n)
  k = len(div)
  L = xrange(n)
  T = [[False for i in xrange(n+1)] for i in xrange(k+1)]

  for i in xrange(k+1):
    T[i][0] = True
  
  for i in xrange(1,k+1):
    for j in xrange(1,n+1):
      if j < div[i-1]:
        T[i][j] = T[i-1][j]
      else:
        T[i][j] = T[i-1][j] or T[i-1][j-div[i-1]]
  
  return T[k][n]  
    
"""
  Return True if the number is abundant
"""
def abundant(n):
  return sum(divisors(n)) > n


"""
  Remove all multiples of n from L, returning a new list
"""
def seive(L, n):
  return [i for i in L if i%n!=0]

"""
  Lemma: For integers n and m, if n is abundant and not weird and n divides m then m is not weird
  Proof:
  
"""
def weird_num(n):
  W = []
  L = list(xrange(2,n))
  while len(L):
    x = L.pop(0)
    ab = abundant(x)
    
    if ab:
      sp = semiperfect(x)
      if sp: L = seive(L, x)
      else: W.append(x)
  return W

class WeirdNumberTests(unittest.TestCase):
  def test_divisors(self):
    self.assertEquals(divisors(2), [1])
    self.assertEquals(divisors(6), [1,2,3])
    self.assertEquals(divisors(7), [1])
    self.assertEquals(divisors(18), [1,2,3,6,9])
    
  def test_semiperfect(self):
    self.assertTrue(semiperfect(6))
    self.assertFalse(semiperfect(7)) 
    
  def test_abundant(self):
    self.assertTrue(abundant(12))
    self.assertFalse(abundant(8))
  
  def test_seive(self):
    L= [1,2,4,5,7,8]
    self.assertEquals(seive(list(xrange(10)), 3), L)
  
  def test_weird_num(self):
    L = [70, 836]
    self.assertEquals(weird_num(1000), L)
    
unittest.main(argv=['first-arg-is-ignored'], exit=False)


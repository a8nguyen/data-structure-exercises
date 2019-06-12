import numpy as np
import unittest
#import time

"""
Write a Captcha system that uses english-based math questions to distinguish
humans from bots.
"""

"""
Chunk a number in three
"""
def chunking(num):
    L = [str(num)[::-1][i:i+3] for i in xrange(0, len(str(num)), 3)]
    return [int(x[::-1]) for x in L[::-1]]

"""
Name by thousands
"""
def name_by_thousand(num):
    thousandList = ['', 'thousand', 'million', 'billion', 'trillion', 'quadrillion']
    return thousandList[0:len(chunking(num))][::-1]

"""
Convert a number into English numerals
"""
def num2hum(n):
    numDict = {0: '', 1: 'one', 2: 'two',
        3: 'three', 4: 'four', 5: 'five',
        6: 'six', 7: 'seven', 8: 'eight',
        9: 'nine', 10: 'ten', 11: 'eleven',
        12: 'twelve', 13: 'thirteen', 14: 'fourteen',
        15: 'fifteen', 16:'sixteen', 17: 'seventeen',
        18: 'eighteen', 19: 'nineteen', 20: 'twenty',
        30: 'thirty', 40: 'forty', 50: 'fifty',
        60: 'sixty', 70: 'seventy', 80: 'eighty',
        90: 'ninety'}

    if n == 0: return 'zero'
    empty = []
    for j in range(0, len(chunking(n))):
        empty.append([])
        i = chunking(n)[j]
        if i in numDict:
            if i in range(1,100) and j != 0: empty[j] = empty[j] + ['and ' + numDict[i]]
            else: empty[j] = empty[j] + [numDict[i]]
        else:
            if i//100 != 0:
                empty[j] = empty[j] + [numDict[i//100] + ' hundred']
            if i%100 > 9:
                if 10<i%100< 20:
                    if i//100 == 0: empty[j] = empty[j] + [numDict[i%100]]
                    else: empty[j] = empty[j] + ['and ' + numDict[i%100]]
                elif i%10 != 0 and i//10 != 10:
                    if i//100 == 0: empty[j] = empty[j] + [numDict[np.ceil((i%100)/10)*10] + '-' + numDict[i%10]]
                    else: empty[j] = empty[j] + ['and ' + numDict[np.ceil((i%100)/10)*10] + '-' + numDict[i%10]]
                else: empty[j] = empty[j] + ['and ' + numDict[np.ceil((i%100)/10)*10]]
            if i%10 != 0 and i%100<9:
                empty[j] = empty[j] + ['and ' + numDict[i%10]]
        if empty[j] != ['']: empty[j].append(name_by_thousand(n)[j])
    empty[-1].pop()
    return ' '.join([item for sublist in empty for item in sublist])

def load_captchas(fn):
    captchas = []
    with open(fn,'r') as capfile:
        for line in capfile:
            english, vals, python = line.split(';')
            captchas.append((english, int(vals), python))
    return captchas

def eval_captcha(cap, values):
    english, num_vals, python = cap
    assert num_vals==len(values)

    text_values = [num2hum(v) for v in values]
    english = english.format(*text_values)
    answer = eval(python.format(*[str(v) for v in values]))

    return english, answer

def generate_captcha(number=None, fn='captchas'):
    captcha = load_captchas(fn)
    if number is None:
        number = np.random.randint(0,len(captcha))
    i = captcha[number-1]
    num = sorted(np.random.random_integers(1000, size= int(i[1])))
    captcha, answer = eval_captcha(i, num)
    return captcha, answer


class MathCaptcha(unittest.TestCase):
  def test_chunking(self):
      self.assertEquals(chunking(180), [180])
      self.assertEquals(chunking(2002), [2, 2])

  def test_name_by_thousand(self):
      self.assertEquals(name_by_thousand(180), [''])
      self.assertEquals(name_by_thousand(1180), ['thousand', ''])

  def test_num2hum(self):
      self.assertEquals(num2hum(2), 'two')
      self.assertEquals(num2hum(22), 'twenty-two')
      self.assertEquals(num2hum(2002), 'two thousand and two')
      self.assertEquals(num2hum(1876), 'one thousand eight hundred and seventy-six')
  def test_generate_captcha(self):
      captcha, answer = generate_captcha(number=1)
      assert type(answer) is int
      assert 'What is' in captcha and 'times' in captcha and '{0}' not in captcha and '{1}' not in captcha, captcha

  def test_eval_captcha(self):
      cap = load_captchas('captchas')[1]
      exp_str = "How many sheep are left when a wolf eats one hundred and three from a flock of seventy-six thousand two hundred and thirty-four?"
      exp_ans = 76131
      self.assertEquals(eval_captcha(cap, [103, 76234]), (exp_str, exp_ans))

      exp_str = "How many sheep are left when a wolf eats one hundred and thirteen from a flock of seventy-six?"
      exp_ans = 0
      self.assertEquals(eval_captcha(cap, [113, 76]), (exp_str, exp_ans))

unittest.main(argv=['first-arg-is-ignored'], exit=False)

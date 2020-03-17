import click
import unittest
import string
_dictfile = "/usr/share/dict/words"                     #dictionary comes from Ubuntu on Mac and/or Linux. Window users might have the list of words elsewhere.

# Challenges:
# 0. Complete the task as written
# 1. Allow insertions and deletions

class NoSuchPathError(Exception):
    pass

class Dictionary(object):
    def __init__(self, n=_dictfile):
        self._indices = {} # dictionary of word -> integer
        self._reverse = {}
        # load words from the dictionary, ignore case
        with open(_dictfile, 'r') as df:
            for i, line in enumerate(df):
                w = line.strip().lower()
                self._indices[w] = i
                self._reverse[i] = w
        self._neighbors = {} # dictionary of integer -> list(integers)
        # find all adjacent words
        with click.progressbar(self._indices.keys()) as pb:
            for w in pb:
                i = self._indices[w]
                self._neighbors[i] = list()

                for j, c in enumerate(w):
                    for a in string.ascii_lowercase:
                        if c is a: continue
                        news = w[:j] + a + w[j+1:]
                        if news in self._indices: self._neighbors[i].append(self._indices[news])

    def __iter__(self):
        for w in self._indices:
            yield w

    def __len__(self):
        return len(self._indices)

    def keys(self):
        return self._indices.keys()

    def __hasitem__(self, w):
        # check if w in the dictionary
        return w in self._indices

    def __getitem__(self, w):
        return [self._reverse[j] for j in self._neighbors[self._indices[w]]]


def find_path(w1, w2, D):
    if w1 is w2:
        return [w1]

    queue = [w1]
    ancestors = {}

    while queue:
        u = queue.pop(0)
        for v in D[u]:
            if v not in ancestors:
                ancestors[v] = u
                queue.append(v)
            if v == w2:
                break

    path = [w2]
    word = w2
    while word != w1:
        word = ancestors[word]
        path.append(word)
    path.reverse()
    return path

class Test_WordChain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.word_dict = Dictionary()

    def test_dictionary(self):
        D = Test_WordChain.word_dict
        self.assertEquals(len(D), 234371)

        assert 'word' in D
        assert 'duck' in D
        assert 'ruby' in D
        assert 'Washington' not in D
        assert 'washington' in D

        self.assertEquals(D['lack'], ['lick', 'luck', 'lock', 'rack', 'pack', 'tack', 'back', 'hack', 'sack', 'lace', 'lacy'])

    def test_find_path(self):
        D = Test_WordChain.word_dict
        words = find_path('duck', 'ruby', D)
        for w in words:
            assert w in D
        for w1,w2 in zip(words, words[1:]):
            assert w2 in D[w1]
        self.assertEquals(len(words), 6)
        print words

    def test_find_path_when_none_exists(self):
        D = Test_WordChain.word_dict
        try:
            find_path('duck', 'leg', D)
        except NoSuchPathError:
            pass
        else:
            assert "Expected ValueError for non existent path duck -> leg"

        try:
            find_path('duck', 'cixo', D)
        except NoSuchPathError:
            pass
        else:
            assert "Expected ValueError for non existent path duck -> "

unittest.main(argv=['first-arg-is-ignored'],exit = False)

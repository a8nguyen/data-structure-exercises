import unittest

class LexicalError(Exception):
    pass

class GrammarError(Exception):
    pass

class Node(object):
    def __init__(self, ntype, parent):
        self._ntype = ntype
        self._parent = parent
        if parent is not None:
            parent.add_child(self)
        self._children = []

    def add_child(self, child):
        self._children.append(child)

    @property
    def parent(self):
        return self._parent

    def __str__(self):
        return self._print()

    def _print(self, level=0):
        return '\n'.join([('   ' * level) + self._ntype] + [c._print(level=level+1) for c in self._children])

class Expression(object):
    def __init__(self, expr):
        # parse string integer arithmetic expression containing ( ) + - * /
        self.expr = expr
        self._tokens = self._tokenize()
        self._tree = self._parse()

    def _tokenize(self):
        token = []
        expr = list(self.expr) + ['eof']
        digits = '0123456789'
        state = None
        buf = ''

        i=0
        while i<len(expr):
            c = expr[i]
            if state == 'number':
                if c in digits:
                    buf += c
                else:
                    state = None
                    token.append(('num', int(buf)))
                    i-=1
            elif state is None:
                if c in digits:
                    buf = ''+c
                    state = 'number'
                elif c in '/*+-':
                    token.append(('op', c))
                elif c == '(':
                    token.append(('open', c))
                elif c == ')':
                    token.append(('close', c))
                elif c in [' ', '\t', 'eof']:
                    pass
                else:
                    raise LexicalError("Unrecognized token at position %d: %s" % (i, c))
            i+=1
        return token

    def _parse(self):
        self._stream = self._tokens
        self._cnode = Node('x', None)
        self._E()

    def _add_child(self, ntype):
        self._cnode = Node(ntype, self._cnode)

    def _up(self):
        self._cnode = self._cnode.parent

    def _consume(self, expectation=None):
        t, v = self._stream[0]
        if expectation is not None and t!=expectation:
            raise SyntaxError("Expected token type %s but saw %s" % (expectation, t))
        self._stream = self._stream[1:]
        return v

    def _empty(self):
        return len(self._stream)==0

    def _peek(self):
        return self._stream[0][0]

    def _E(self):
        print 'E'
        self._add_child('E')
        self._F()
        self._Ep()
        self._up()

    def _Ep(self):
        print 'Ep'
        self._add_child('Ep')
        if self._empty():
            pass
        elif self._peek() == 'op':
            self._consume('op')
            self._F()
            self._Ep()
        self._up()

    def _F(self):
        print 'F'
        self._add_child('F')
        if self._peek()=='num':
            num = self._consume('num')
        elif self._peek()=='open':
            self._consume('open')
            rval = self._E()
            self._consume('close')
        else:
            raise SyntaxError("Encountered unexpected token: %s" % (self._peek()))
        self._up()

    @property
    def tree(self):
        return self._tree

    def __str__(self):
        """ Convert the parse tree to a python compatible string expression """
        pass

    def simplify(self):
        """ Remove redundant nesting from the parse tree """
        pass


class TestExpression(unittest.TestCase):
    def test_expression(self):
        input = "((3 + 1) * ((5 + 4) * 25))"
        expr = Expression(input)
        self.assertEquals(expr.tree, ('*', ('+', 3, 1), ('*', ('+', 5, 4), 25)))
        expr.simplify()
        self.assertEquals(expr.tree, ('*', ('+', 3, 1), ('+', 5, 4), 25))
        self.assertEquals(str(expr), "((3 + 1) * (5 + 4) * 25)")

    def test_parse_tree(self):
        input = "(3+1) * ( 5 - 3 )"
        expr = Expression(input)
        self.assertEquals(expr.tree, ('*', ('+', 3, 1), ('-', 5, 3)))

    def test_parse_tree_error(self):
        input = "(3+1) * "
        with self.assertRaises(GrammarError):
            expr = Expression(input)

    def test_lexical_tokens(self):
        input = "((3 + 1) * ((5 + 4) * 25))"
        expr = Expression(input)
        expected_tokens = [('open','('),
                                ('open','('), ('num',3), ('op','+'), ('num',1), ('close',')'),
                                ('op','*'),
                                ('open','('),
                                     ('open','('), ('num', 5), ('op', '+'), ('num',4), ('close',')'),
                                     ('op','*'),
                                     ('num', 25),
                                ('close', ')'),
                           ('close',')')]
        self.assertEquals(expr._tokenize(), expected_tokens)

    def test_lexical_parser_error_on_bad_token(self):
        input = "((3.+ 1) * ((5 + 4) * 25))"

        with self.assertRaises(LexicalError) as e:
            expr=Expression(input)
            assert e.message == 'Unrecognized token at position 3: .'


#unittest.main(argv=['first-arg-is-ignored'], exit=False)

input = "(3+1) * ( 5 - 3 )"
e = Expression(input)
print "Parse tree:"
print e._cnode

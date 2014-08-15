#!/usr/bin/env python

import unittest
import objectTracer
import StringIO


class A (object):
    def __init__(self, a):
        self.a = a
    def add(self, x):
        self.a += x
        return self.a
    def addn(self, x, n):
        for i in range(n):
            self.add(x)


def secret_method(x):
    x.add(1)
    x.addn(2, 2)
    x.b = 3
    del(x.b)


class TestNewTypeObject(unittest.TestCase):

    def setUp(self):
        self.out = StringIO.StringIO()

    def test_access_to_variables(self):
        a = A(5)
        objectTracer.instrument(a, name='a', stream=self.out)
        a.a = 2
        a.a
        del(a.a)
        objectTracer.clean(a)
        self.assertEqual(self.out.getvalue(),
                         "a.a < 2\n"
                         "a.a > 2\n"
                         "del(a.a)\n")

    def test_basic_method_call(self):
        a = A(5)
        objectTracer.instrument(a, name='a', stream=self.out)
        a.add(2)
        objectTracer.clean(a)
        self.assertEqual(self.out.getvalue(),
                         '> a.add(2)\n'
                         '  a.a > 5\n'
                         '  a.a < 7\n'
                         '  a.a > 7\n'
                         '< 7\n')

    def test_method_call(self):
        a = A(5)
        objectTracer.instrument(a, name='a', stream=self.out)
        secret_method(a)
        objectTracer.clean(a)
        self.assertEqual(self.out.getvalue(),
                         '> a.add(1)\n'
                         '  a.a > 5\n'
                         '  a.a < 6\n'
                         '  a.a > 6\n'
                         '< 6\n'
                         '> a.addn(2, 2)\n'
                         '  > a.add(2)\n'
                         '    a.a > 6\n'
                         '    a.a < 8\n'
                         '    a.a > 8\n'
                         '  < 8\n'
                         '  > a.add(2)\n'
                         '    a.a > 8\n'
                         '    a.a < 10\n'
                         '    a.a > 10\n'
                         '  < 10\n'
                         '< None\n'
                         'a.b < 3\n'
                         'del(a.b)\n')


if __name__ == '__main__':
    unittest.main()
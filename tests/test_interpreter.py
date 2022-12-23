from ilib.interpreter import Interpreter
import pytest


class TestInterpreter:
    def test_interpreter(self):
        interpreter = Interpreter()

        with open('tests/data/test1.txt') as f:
            test = f.read()
            assert interpreter.eval(test) == ''

        with open('tests/data/test2.txt') as f:
            test = f.read()
            assert interpreter.eval(test) == ''

        with open('tests/data/test3.txt') as f:
            test = f.read()
            assert interpreter.eval(test) == ''

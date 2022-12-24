from ilib.interpreter import Interpreter
import pytest


class TestInterpreter:
  inter = Interpreter()

  def test_interpreter(self):
    with open('tests/data/test1.txt', 'r') as f:
      text = f.read()
      assert self.inter.eval(text) == {}

    with open('tests/data/test2.txt', 'r') as f:
      test = f.read()
      assert self.inter.eval(test) == {'x': 17.0, 'y': 11.0}

    with open('tests/data/test3.txt', 'r') as f:
      test = f.read()
      assert self.inter.eval(test) == {'x': 11.0, 'y': 2.0, 1: {
          'a': 3.0, 'b': 18.0, 'c': -15.0}}

  def test_lexer(self):
    ...

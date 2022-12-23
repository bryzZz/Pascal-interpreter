from .tokens import Token, TokenType, Words
from .utils import isLetter


class LexerException(Exception):
  ...


class Lexer:
  def __init__(self):
    self.pos = 0
    self.text = ""
    self.current_char = ''
    self.prev_char = ''

  def init_lexer(self, text: str):
    self.pos = 0
    self.text = text
    self.current_char = self.text[self.pos]

  def skip(self):
    while self.current_char != "" and self.current_char.isspace():
      self.forward()

  def number(self) -> str:
    result = []

    while self.current_char != '' and self.current_char.isdigit() or self.current_char == '.':
      result.append(self.current_char)
      self.forward()

    return "".join(result)

  def word(self, expected_word: Words) -> str:
    result = []

    for char in expected_word.value[0]:
      if char == self.current_char:
        result.append(self.current_char)
        self.forward()
      else:
        raise LexerException(f'Incorrect {expected_word.value} word')

    return "".join(result)

  def assign(self) -> str:
    result = []

    result.append(self.current_char)
    self.forward()

    if self.current_char == '=':
      result.append(self.current_char)
      self.forward()
    else:
      raise LexerException(f'Incorrect assignment')

    return "".join(result)

  def identifier(self) -> str:
    result = []

    while isLetter(self.current_char):
      result.append(self.current_char)
      self.forward()

    return "".join(result)

  def forward(self):
    self.prev_char = self.text[self.pos]  # save previous char

    self.pos += 1
    if self.pos == len(self.text):
      self.current_char = ''
    else:
      self.current_char = self.text[self.pos]

  def next(self) -> Token:
    while self.current_char != '':
      if self.current_char.isspace():
        self.skip()
        continue

      # program
      if self.current_char == Words.BEGIN.value[0][0]:
        return Token(TokenType.BEGIN, self.word(Words.BEGIN))

      if self.current_char == Words.END.value[0][0]:
        return Token(TokenType.END, self.word(Words.END))

      if isLetter(self.current_char):
        return Token(TokenType.ID, self.identifier())

      if self.current_char == '.':
        ch = self.current_char
        self.forward()
        return Token(TokenType.DOT, ch)

      if self.current_char == ';':
        ch = self.current_char
        self.forward()
        return Token(TokenType.SEMI, ch)

      if self.current_char == ':':
        return Token(TokenType.ASSIGN, self.assign())

      # math below
      if self.current_char.isdigit():
        return Token(TokenType.NUMBER, self.number())
      if self.current_char == "+":
        ch = self.current_char
        self.forward()
        return Token(TokenType.PLUS, ch)
      if self.current_char == "-":
        ch = self.current_char
        self.forward()
        return Token(TokenType.MINUS, ch)
      if self.current_char == "*":
        ch = self.current_char
        self.forward()
        return Token(TokenType.MUL, ch)
      if self.current_char == "/":
        ch = self.current_char
        self.forward()
        return Token(TokenType.DIV, ch)
      if self.current_char == "(":
        ch = self.current_char
        self.forward()
        return Token(TokenType.LPAREN, ch)
      if self.current_char == ")":
        ch = self.current_char
        self.forward()
        return Token(TokenType.RPAREN, ch)

      raise LexerException(f'bad token {self.current_char}')
    return Token(TokenType.EOL, "")

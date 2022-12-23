from enum import Enum, auto


class Words(Enum):
  BEGIN = "BEGIN",
  END = "END",


class TokenType(Enum):
  BEGIN = auto()
  END = auto()
  DOT = auto()
  SEMI = auto()
  ID = auto()
  ASSIGN = auto()
  NUMBER = auto()
  PLUS = auto()
  MINUS = auto()
  DIV = auto()
  MUL = auto()
  EOL = auto()
  LPAREN = auto()
  RPAREN = auto()


class Token:
  def __init__(self, type: TokenType, value: str) -> None:
    self.type = type
    self.value = value

  def __str__(self) -> str:
    return f"Token {self.type}, {self.value}"

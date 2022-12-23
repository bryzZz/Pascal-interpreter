from tokens import Token, TokenType
from lexer import Lexer
from tree import Node, BinOp, UnaryOp, Number, Statement, StatementList


class ParserException(Exception):
  ...


class Parser:
  def __init__(self):
    self.current_token: Token | None = None
    self.lexer = Lexer()

  def check_type(self, type_: TokenType):
    if (self.current_token is None):
      raise ParserException("Current token is not defined")

    if self.current_token.type == type_:
      self.current_token = self.lexer.next()
      return

    raise ParserException(
        f"invalid token order. Expected {type_}, Received {self.current_token.type}")

  def factor(self) -> Node:
    if (self.current_token is None):
      raise ParserException("Current token is not defined")

    token = self.current_token

    if token.type == TokenType.NUMBER:
      self.check_type(TokenType.NUMBER)
      return Number(token)
    elif token.type == TokenType.MINUS:
      self.check_type(TokenType.MINUS)
      result = self.factor()
      return UnaryOp(token, result)
    elif token.type == TokenType.PLUS:
      self.check_type(TokenType.PLUS)
      result = self.factor()
      return UnaryOp(token, result)
    elif token.type == TokenType.LPAREN:
      self.check_type(TokenType.LPAREN)
      result = self.expr()
      self.check_type(TokenType.RPAREN)
      return result

    raise ParserException(f"Invalid factor {token}")

  def term(self) -> Node:
    if (self.current_token is None):
      raise ParserException("Current token is not defined")

    ops = [TokenType.MUL, TokenType.DIV]
    result = self.factor()

    while self.current_token.type in ops:
      token = self.current_token
      match token.type:
        case TokenType.DIV:
          self.check_type(TokenType.DIV)
        case TokenType.MUL:
          self.check_type(TokenType.MUL)

      result = BinOp(result, token, self.factor())

    return result

  def expr(self) -> Node:
    if (self.current_token is None):
      raise ParserException("Current token is not defined")

    ops = [TokenType.MINUS, TokenType.PLUS]
    result = self.term()

    while self.current_token.type in ops:
      token = self.current_token
      match token.type:
        case TokenType.PLUS:
          self.check_type(TokenType.PLUS)
        case TokenType.MINUS:
          self.check_type(TokenType.MINUS)

      result = BinOp(result, token, self.term())

    return result

  def statement(self):
    if (self.current_token is None):
      raise ParserException("Current token is not defined")

    id = self.current_token

    self.check_type(TokenType.ID)
    self.check_type(TokenType.ASSIGN)

    expression = self.expr()

    return Statement(id, expression)

  def statement_list(self):
    if (self.current_token is None):
      raise ParserException("Current token is not defined")

    st_list = StatementList()

    match self.current_token.type:
      case TokenType.BEGIN:
        ...
      case TokenType.ID:
        statement = self.statement()
        st_list.addStatement(statement)

        self.check_type(TokenType.SEMI)

        if self.current_token.type == TokenType.ID:
          st_list.statements.extend(
              self.statement_list().statements)  # type: ignore

        return st_list

  def complex_statement(self):
    if (self.current_token is None):
      raise ParserException("Current token is not defined")

    self.check_type(TokenType.BEGIN)

    result = self.statement_list()

    self.check_type(TokenType.END)

    return result

  def program(self):
    if (self.current_token is None):
      raise ParserException("Current token is not defined")

    result = self.complex_statement()

    if self.current_token.type == TokenType.DOT:
      return result

    raise ParserException("Expercted dot at the very end")

  def init_parser(self, text: str) -> None:
    self.lexer.init_lexer(text)
    self.current_token = self.lexer.next()

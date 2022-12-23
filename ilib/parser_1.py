from .tokens import Token, TokenType
from .lexer import Lexer
from .tree import Node, BinOp, UnaryOp, Number, ComplexStatement, StatementList, Statement, Variable


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

    if token.type == TokenType.ID:
      self.check_type(TokenType.ID)
      return Variable(token)

    if token.type == TokenType.NUMBER:
      self.check_type(TokenType.NUMBER)
      return Number(token)

    if token.type == TokenType.MINUS:
      self.check_type(TokenType.MINUS)
      result = self.factor()
      return UnaryOp(token, result)

    if token.type == TokenType.PLUS:
      self.check_type(TokenType.PLUS)
      result = self.factor()
      return UnaryOp(token, result)

    if token.type == TokenType.LPAREN:
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

  def statement_list(self, st_list: StatementList | None = None):
    if (self.current_token is None):
      raise ParserException("Current token is not defined")

    if not st_list:
      st_list = StatementList()

    if self.current_token.type == TokenType.END:
      return st_list

    st_list.addStatement(self.statement())

    self.check_type(TokenType.SEMI)

    if self.current_token.type == TokenType.ID:
      st_list.statements.extend(
          self.statement_list().statements)  # type: ignore

    return st_list

  def complex_statement(self, parent: ComplexStatement | None = None, current_closure: ComplexStatement | None = None):
    if (self.current_token is None):
      raise ParserException("Current token is not defined")

    result = None

    if current_closure:
      self.statement_list(current_closure.statement_list)
      result = current_closure

    if self.current_token.type == TokenType.BEGIN:
      self.check_type(TokenType.BEGIN)
      result = ComplexStatement(self.statement_list(), parent)

    if self.current_token.type == TokenType.BEGIN and result:
      result.addComplexStatement(
          self.complex_statement(result))  # type: ignore

    if self.current_token.type == TokenType.END:
      self.check_type(TokenType.END)

    if self.current_token.type == TokenType.SEMI:
      self.check_type(TokenType.SEMI)
      self.complex_statement(current_closure=parent)

    return result

  def program(self):
    if (self.current_token is None):
      raise ParserException("Current token is not defined")

    complex_statement = self.complex_statement()

    if self.current_token.type == TokenType.DOT:
      return complex_statement

    raise ParserException("Expercted dot at the very end")

  def init_parser(self, text: str) -> None:
    self.lexer.init_lexer(text)
    self.current_token = self.lexer.next()

from abc import ABC
from tokens import Token


class Node(ABC):
  ...


class Number(Node):
  def __init__(self, value: Token) -> None:
    self.value = value

  def __str__(self) -> str:
    return f"{self.__class__.__name__}({self.value})"


class BinOp(Node):
  def __init__(self, left: Node, op: Token, right: Node) -> None:
    self.left = left
    self.op = op
    self.right = right

  def __str__(self) -> str:
    return f"BinOp {self.op.value}, {self.left}, {self.right}"


class UnaryOp(Node):
  def __init__(self, op: Token, right: Node) -> None:
    self.op = op
    self.right = right

  def __str__(self) -> str:
    return f"UnOp {self.op.value}, {self.right}"


class Variable(Node):
  def __init__(self, value: Token) -> None:
    self.value = value

  def __str__(self) -> str:
    return f'Variable {self.value}'


class Statement(Node):
  def __init__(self, id: Token, expression: Node) -> None:
    self.id = id
    self.expression = expression

  def __str__(self) -> str:
    return f"Statement {self.id.value}, {self.expression}"


class StatementList(Node):
  def __init__(self) -> None:
    self.statements = []

  def addStatement(self, statement: Statement):
    self.statements.append(statement)

  def __str__(self) -> str:
    return "StatementList \n" + "\n".join([str(st) for st in self.statements])


class ComplexStatement(Node):
  def __init__(self, statement_list: StatementList, parent) -> None:
    self.statement_list = statement_list
    self.nest_complex_statements = []
    self.parent = parent
    self.variables = dict()

  def addComplexStatement(self, complexStatement: "ComplexStatement"):
    self.nest_complex_statements.append(complexStatement)

  def __str__(self) -> str:
    return "ComplexStatement:" + "\n" + str(self.statement_list) + "\n" + "\n".join([str(st) for st in self.nest_complex_statements])


class NodeVisitor:
  def visit(self, node: Node) -> float:
    raise NotImplementedError

from parser_1 import Parser
from tree import Node, Number, BinOp, UnaryOp, StatementList, Statement, NodeVisitor
from tokens import TokenType


class InterpreterException(Exception):
  ...


class Interpreter(NodeVisitor):
  def __init__(self):
    self.parser = Parser()
    self.variables = {}

  def visit(self, node: Node) -> float | None:
    if isinstance(node, StatementList):
      return self.visit_statement_list(node)

    if isinstance(node, Statement):
      return self.visit_statement(node)

    if isinstance(node, Number):
      return self.visit_number(node)

    if isinstance(node, BinOp):
      return self.visit_bin_op(node)

    if isinstance(node, UnaryOp):
      return self.visit_unary_op(node)

    raise IndentationError("Invalid Node")

  def visit_number(self, node: Number) -> float:
    return float(node.value.value)

  def visit_bin_op(self, node: BinOp) -> float:
    match node.op.type:
      case TokenType.PLUS:
        return self.visit(node.left) + self.visit(node.right)  # type: ignore
      case TokenType.MINUS:
        return self.visit(node.left) - self.visit(node.right)  # type: ignore
      case TokenType.MUL:
        return self.visit(node.left) * self.visit(node.right)  # type: ignore
      case TokenType.DIV:
        return self.visit(node.left) / self.visit(node.right)  # type: ignore

    raise InterpreterException("Invalid operator")

  def visit_unary_op(self, node: UnaryOp) -> float:
    if (node.op.type == TokenType.MINUS or node.op.type == TokenType.PLUS):
      return self.visit(node.right) * -1  # type: ignore

    raise InterpreterException("Invalid binary operator")

  def visit_statement(self, node: Statement):
    self.variables[node.id.value] = self.visit(node.expression)

  def visit_statement_list(self, node: StatementList):
    for st in node.statements:
      self.visit_statement(st)

  def eval(self, text: str):
    self.parser.init_parser(text)
    tree = self.parser.program()

    self.visit(tree)  # type: ignore

    print(tree)
    print(self.variables)


intr = Interpreter()
# intr.eval("BEGIN\nEND.")

# intr.eval("BEGIN\nx:= 2;\ny:= 2;\nEND.")

intr.eval(
    "BEGIN\nx:= 2 + 3 * (2 + 3);\ny:= 2 / 2 - 2 + 3 * ((1 + 1) + (1 + 1));\nEND.")

# intr.eval("-1.2 - 3")

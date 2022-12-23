from .parser_1 import Parser
from .tree import NodeVisitor, Node, Number, BinOp, UnaryOp, ComplexStatement, StatementList, Statement, Variable
from .tokens import TokenType


class InterpreterException(Exception):
  ...


class Interpreter(NodeVisitor):
  def __init__(self):
    self.parser = Parser()
    self.current_complex_statement = None
    self.scope_id = 0

  def visit(self, node: Node) -> float | None:
    if isinstance(node, ComplexStatement):
      return self.visit_complex_statement(node)

    if isinstance(node, StatementList):
      return self.visit_statement_list(node)

    if isinstance(node, Statement):
      return self.visit_statement(node)

    if isinstance(node, Variable):
      return self.visit_variable(node)

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

  def visit_variable(self, node: Variable):
    complex_statement = self.current_complex_statement
    var_name = node.value.value

    while complex_statement != None:
      if var_name in complex_statement.variables.keys():
        return float(complex_statement.variables[var_name])

      complex_statement = complex_statement.parent

    raise InterpreterException(f'"{var_name}" does not exist in this scope')

  def visit_statement(self, node: Statement):
    self.current_complex_statement.variables[node.id.value] = self.visit(  # type: ignore
        node.expression)

  def visit_statement_list(self, node: StatementList):
    for st in node.statements:
      self.visit_statement(st)

  def visit_complex_statement(self, node: ComplexStatement):
    self.current_complex_statement = node

    self.visit_statement_list(node.statement_list)

    for ncs in node.nest_complex_statements:
      self.visit_complex_statement(ncs)

  def get_variables(self, node: ComplexStatement, result={}):
    for var in node.variables:
      result[var] = node.variables[var]

    for cs in node.nest_complex_statements:
      self.scope_id += 1
      result[self.scope_id] = self.get_variables(cs, {})

    return result

  def eval(self, text: str):
    self.current_complex_statement = None
    self.scope_id = 0
    self.parser.init_parser(text)

    tree = self.parser.program()

    self.visit(tree)  # type: ignore

    return self.get_variables(tree)  # type: ignore

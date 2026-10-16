"""Safe string-expression calculator built on the ast module."""

import ast
import operator
import sys

MAX_LENGTH = 200
MAX_EXPONENT = 1000

BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):
            return node.value
        raise ValueError(f"Unsupported value: {node.value!r}")

    if isinstance(node, ast.BinOp):
        op = BINARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        left = _eval(node.left)
        right = _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > MAX_EXPONENT:
            raise ValueError(f"Exponent too large (max {MAX_EXPONENT})")
        try:
            return op(left, right)
        except ZeroDivisionError:
            raise ValueError("Division by zero") from None
        except OverflowError:
            raise ValueError("Result too large") from None

    if isinstance(node, ast.UnaryOp):
        op = UNARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op(_eval(node.operand))

    raise ValueError(f"Unsupported expression: {type(node).__name__}")


def calculate(expression: str):
    """Evaluate an arithmetic expression string and return the result."""
    print("Calculator Tool Called: ",expression)
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")
    if len(expression) > MAX_LENGTH:
        raise ValueError(f"Expression too long (max {MAX_LENGTH} characters)")
    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError:
        raise ValueError("Invalid expression") from None
    return _eval(tree.body)


def main():
    if len(sys.argv) < 2:
        print('Usage: python calculator.py "<expression>"', file=sys.stderr)
        sys.exit(2)
    try:
        print(calculate(" ".join(sys.argv[1:])))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

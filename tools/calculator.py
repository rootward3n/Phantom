"""
tools/calculator.py
Safe arithmetic tool.
"""

from __future__ import annotations

import ast
import operator as op

from tools.base import Tool


_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        operator = _ALLOWED_OPERATORS[type(node.op)]
        return operator(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        operator = _ALLOWED_OPERATORS[type(node.op)]
        return operator(operand)

    raise ValueError("Unsupported expression")


class CalculatorTool(Tool):
    name = "calc"
    description = "Perform safe arithmetic calculations."

    def execute(self, arguments: str) -> str:
        expression = arguments.strip()

        if not expression:
            return "Usage: /calc <expression>"

        try:
            tree = ast.parse(expression, mode="eval")
            result = _safe_eval(tree.body)
            return str(result)
        except ZeroDivisionError:
            return "Error: Division by zero."
        except Exception as e:
            return f"Calculation error: {e}"

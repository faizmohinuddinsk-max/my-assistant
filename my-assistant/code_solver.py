import io
import contextlib

import sympy
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)

TRANSFORMS = standard_transformations + (implicit_multiplication_application,)


def run_code(code):
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code, {"__builtins__": __builtins__})
    except Exception as e:
        return f"Error: {e}"

    result = output.getvalue().strip()
    return result if result else "Ran with no output."


def solve_equation(equation_text):
    equation_text = equation_text.replace("^", "**")

    symbols_found = sorted(set(
        ch for ch in equation_text if ch.isalpha()
    ))
    if not symbols_found:
        return "I couldn't find a variable to solve for."

    syms = sympy.symbols(" ".join(symbols_found))
    if not isinstance(syms, (list, tuple)):
        syms = (syms,)

    try:
        if "=" in equation_text:
            left, right = equation_text.split("=", 1)
            expr = sympy.Eq(
                parse_expr(left, transformations=TRANSFORMS),
                parse_expr(right, transformations=TRANSFORMS)
            )
        else:
            expr = parse_expr(equation_text, transformations=TRANSFORMS)

        solution = sympy.solve(expr, syms)
    except Exception as e:
        return f"Couldn't solve that: {e}"

    return f"Solution: {solution}"

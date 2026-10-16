import pytest

from calculator import calculate


@pytest.mark.parametrize("expr, expected", [
    ("2+3*4", 14),
    ("(2+3)*4", 20),
    ("2**3**2", 512),
    ("-5 + 2", -3),
    ("7//2", 3),
    ("10/4", 2.5),
    ("7 % 3", 1),
    ("2 + 3 * (4 - 1) ** 2", 29),
    ("  1.5 * 2 ", 3.0),
    ("--3", 3),
])
def test_valid(expr, expected):
    assert calculate(expr) == expected


@pytest.mark.parametrize("expr", [
    "1/0",
    "2 +",
    "",
    "__import__('os')",
    "abs(1)",
    "x + 1",
    "'a' * 3",
    "True + 1",
    "9**9**9",
    "1 if 1 else 2",
    "1" * 500,
])
def test_invalid(expr):
    with pytest.raises(ValueError):
        calculate(expr)

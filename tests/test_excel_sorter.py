import os
import ast
import re


def load_function(file_path, func_name):
    """Load a function from a Python file without executing the rest of the file."""
    with open(file_path, "r") as f:
        source = f.read()
    module = ast.parse(source)
    func_node = None
    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            func_node = node
            break
    if func_node is None:
        raise ValueError(f"Function {func_name} not found")
    code = compile(ast.Module(body=[func_node], type_ignores=[]), file_path, "exec")
    namespace = {"re": re, "numbers": 0, "alphabets": ""}
    exec(code, namespace)
    return namespace

def test_separateNumbersAlphabets():
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "excel_sorter.py")
    ns = load_function(file_path, "separateNumbersAlphabets")
    ns["separateNumbersAlphabets"]("ABC123")
    assert ns["numbers"] == ["123"]
    assert ns["alphabets"] == ["ABC"]


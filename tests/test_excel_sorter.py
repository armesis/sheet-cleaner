import os
import ast
import re
import importlib
import sys


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


def test_install_and_import(monkeypatch):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "excel_sorter.py")
    ns = load_function(file_path, "install_and_import")

    calls = {"pip": None, "imports": []}

    def fake_import_module(name):
        calls["imports"].append(name)
        if len(calls["imports"]) == 1:
            raise ImportError
        return f"module-{name}"

    def fake_pip_main(args):
        calls["pip"] = args

    monkeypatch.setattr(importlib, "import_module", fake_import_module)
    monkeypatch.setitem(sys.modules, "pip", type("pipmod", (), {"main": fake_pip_main}))

    ns["install_and_import"]("mypkg")

    assert calls["pip"] == ["install", "mypkg"]
    assert ns["mypkg"] == "module-mypkg"


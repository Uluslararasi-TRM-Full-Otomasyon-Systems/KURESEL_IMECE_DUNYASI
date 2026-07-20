import importlib


def test_main_module_imports():
    module = importlib.import_module('main')
    assert callable(module.main)

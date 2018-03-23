from norm.orm.contexts import Demo
from norm.orm.fields import Field


def test_demo():
    assert getattr(Demo, '__table__') == 'Demo'
    mappings = getattr(Demo, '__mappings__')
    assert isinstance(mappings, dict)
    for key, val in mappings.items():
        assert isinstance(key, str)
        assert isinstance(val, Field)
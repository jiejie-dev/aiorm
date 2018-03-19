from norms.models.model_base import Field
from tests.base import Demo

def test_demo():
    assert getattr(Demo, '__table__') == 'Demo'
    mappings = getattr(Demo, '__mappings__')
    assert isinstance(mappings, dict)
    for key, val in mappings.items():
        assert isinstance(key, str)
        assert isinstance(val, Field)
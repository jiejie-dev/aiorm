from sample.models import DemoUser
from aiorm.orm.fields import Field


def test_demo():
    assert getattr(DemoUser, '__table__') == 'DemoUser'
    mappings = getattr(DemoUser, '__mappings__')
    assert isinstance(mappings, dict)
    for key, val in mappings.items():
        assert isinstance(key, str)
        assert isinstance(val, Field)
import logging
import uuid

from norm.models import utils
from norm.models.fields import Field
from norm.query.query_base import QueryImpl

_logger = logging.getLogger('norm')


class ModelMetaclass(type):
    def __getattr__(self, item):
        return QueryImpl(left='{}.{}'.format(getattr(self, '__table__'), item))

    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        table_name = attrs.get('__table__', None) or name
        _logger.info('found model: %s (table: %s)' % (name, table_name))
        mappings = dict()
        fields = []
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                _logger.info('  found mapping: %s ==> %s' % (k, v))
                if v.name is None:
                    v.name = k
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primary_key:
                        raise Exception('Duplicate primary key for field: %s' % k)
                    primary_key = k
                else:
                    fields.append(k)
        if not primary_key:
            raise Exception('Primary key not found in table {}.'.format(table_name))
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名

        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def get_value(self, key):
        return getattr(self, key, None)

    def get_value_or_default(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                _logger.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    def escaped_fields(self):
        return utils.escaped_fields(self.__fields__)

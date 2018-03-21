import logging

from norm.models.fields import ForeignKeyField

_logger = logging.getLogger('norm')


class QueryImpl(object):
    def __init__(self, left=None, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right
        self.args = []

    def name(self):
        return self.left.name() if isinstance(self.left, QueryImpl) else str(self.left)

    def build(self, strs=None, args=None):
        if strs is None:
            strs = []
        if args is None:
            args = []

        if isinstance(self.left, QueryImpl):
            strs.append('(')

        if self.left:
            strs.append(self.name())
        if self.op:
            strs.append(self.op)
        if self.right:
            if isinstance(self.right, QueryImpl):
                strs, args = self.right.build(strs, args)
            else:
                args.append(str(self.right))
                strs.append('?')

        if isinstance(self.left, QueryImpl):
            strs.append(')')

        return ' '.join(strs), args

    def __str__(self):
        return '{}{}{}'.format(self.left, self.op, self.right)

    def __eq__(self, other):
        return QueryImpl(self, '=', other)

    def __le__(self, other):
        return QueryImpl(self, '<=', other)

    def __ge__(self, other):
        return QueryImpl(self, '>=', other)

    def __lt__(self, other):
        return QueryImpl(self, '<', other)

    def __gt__(self, other):
        return QueryImpl(self, '>', other)

    def __and__(self, other):
        return QueryImpl(left=self, op='and', right=other)

    def __or__(self, other):
        return QueryImpl(left=self, op='or', right=other)


class OrderbyImpl(object):
    def __init__(self, field_name, sc='DESC'):
        self.field_name = field_name
        self.sc = sc

    def __str__(self):
        return '{} {}'.format(self.field_name, self.sc)


class OrderbyDescImpl(OrderbyImpl):
    def __init__(self, field_name):
        super(OrderbyDescImpl, self).__init__(field_name, sc='DESC')


class OrderbyAscImpl(OrderbyImpl):
    def __init__(self, field_name):
        super(OrderbyAscImpl, self).__init__(field_name, sc='ASC')


class ResolveJoinRelationRefError(Exception):
    pass


def _foregin_fields(model):
    for key, val in model.__mappings__.items():
        if isinstance(val, ForeignKeyField):
            yield val


def resolve_relation_ref(left, right):
    left_foreign_fields = _foregin_fields(left)
    right_foregin_fields = _foregin_fields(right)

    for item in left_foreign_fields:
        if issubclass(right, item.fk_model):
            return "{}.{}_id".format(left.__table__, item.name), "{}.{}".format(right.__table__, right.__primary_key__)

    for item in right_foregin_fields:
        if issubclass(left, item.fk_model):
            return "{}.{}_id".format(right.__table__, item.name), "{}.{}".format(left.__table__, left.__primary_key__)

    raise ResolveJoinRelationRefError()


class JoinClause(object):
    def __init__(self, left, right, type='INNER'):
        self.left = left
        self.right = right
        self.type = type

    def build(self):
        t = " {type} JOIN {right} ON {left_rel_field} = {right_rel_field}"
        left_rel_field, right_rel_field = resolve_relation_ref(self.left, self.right)

        return t.format(type=self.type,
                        right=self.right.__table__,
                        left_rel_field=left_rel_field,
                        right_rel_field=right_rel_field)


class Query(object):
    """ Represent a query like select, insert, update, delete"""

    def __init__(self, model):
        self.model = model
        self.table_name = getattr(model, '__table__', None)

        self._where = None
        self._orderby = []
        self._limit = 0
        self._offset = 0
        self._include = []

        self._args = []

        self.method = None

        self._join = []

    def select(self):
        self.method = 'SELECT'
        return self

    def update(self):
        self.method = 'UPDATE'
        return self

    def delete(self):
        self.method = 'DELETE'
        return self

    def insert(self, data, **kwargs):
        self.method = 'INSERT'
        self.data = data
        return self

    def include(self, model):
        self._include.append(model)
        return self

    def where(self, query_impl):
        self._where = self._where and query_impl if self._where else query_impl
        return self

    def order_by_asc(self, model_field):
        self._orderby.append(OrderbyAscImpl(model_field))
        return self

    def order_by_desc(self, model_field):
        self._orderby.append(OrderbyDescImpl(model_field))
        return self

    def join(self, model, type="INNER"):
        last_model = self._join[-1].right if len(self._join) > 0 else self.model
        self._join.append(JoinClause(last_model, model, type))
        return self

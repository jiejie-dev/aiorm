import logging

_logger = logging.getLogger('norms')


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


class Query(object):
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

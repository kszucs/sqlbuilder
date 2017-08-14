"""SQL base syntax"""


class SQL:
    """Base for classes that can be rendered as SQL

    Used as a wrapper for primitive values (values and identifiers)
    """

    @staticmethod
    def merge(iterable, sep=', '):
        """Merge an interable of (sql, args) items.

        Returns a single (sql, args) tuple, where the `sql` strings will be
        joined using `sep` argument.
        """

        if iterable is None:
            return '', ()
        iterable = list(iterable)
        if not len(iterable):
            return '', ()
        sql, args = zip(*iterable)
        sql = sep.join(sql)
        args = sum(args, ())
        return sql, args

    @classmethod
    def wrap(cls, value, id=False):
        """Instantiate a `SQL` or `Identifier` instance if `value` is plain"""
        if isinstance(value, SQL):
            return value  # value is already an instance of SQL
        elif id:
            return Identifier(value)
        else:
            return Value(value)

    def _as_sql(self, connection, context):
        raise NotImplementedError()

    def __unicode__(self):
        sql, args = self._as_sql(dummy_connection, dummy_context)
        return sql % args

    def __repr__(self):
        sql, args = self._as_sql(dummy_connection, dummy_context)
        return '<{name} {sql!r}, {args!r}>'.format(
            name=self.__class__.__name__,
            sql=sql,
            args=args,
        )


class SQLIterator(SQL):
    """Iterator of SQL objects"""

    def __init__(self, iterable, sep=', ', id=False):
        self.iterable = iterable
        self.sep = sep
        self.id = id

    def __iter__(self):
        if hasattr(self.iterable, '_as_sql'):
            # iterable knows how to render itself
            yield self.iterable
            return
        for item in self.iterable:
            yield SQL.wrap(item, id=self.id)

    # def iter(self):
    #     return self.__iter__()

    def _as_sql(self, connection, context):
        return SQL.merge((item._as_sql(connection, context) for item in self), sep=self.sep)


from .expression import Identifier, Value
from ..dummy import dummy_connection, dummy_context

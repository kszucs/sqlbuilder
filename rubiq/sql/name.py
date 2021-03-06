from .base import SQL


# this could be a metaclass
def NameFactory(Class, prefix=None, as_sql=None, args=None, kwargs=None):
    """Returns a new class that converts attribute access to Class instances"""

    prefix = prefix or ''
    args = args or ()
    kwargs = kwargs or {}

    def __getattr__(self, name):
        return Class(prefix + name, *args, **kwargs)

    def __setattr__(self, name, value):
        raise AttributeError('Names are not assignable')

    def __call__(self, name):
        return getattr(self, name)

    name = '{classname}Factory'.format(classname=Class.__name__)
    bases = (object,)
    attrs = dict(
        __getattr__=__getattr__,
        __setattr__=__setattr__,
        __call__=__call__,
    )

    if as_sql:
        # create factory that renders as SQL
        attrs['_as_sql'] = as_sql
        bases = (SQL,)

    return type(name, bases, attrs)()


from .expression import Variable, Identifier
from .table import Table, Wildcard

# prepare importable shorthand names for the various name factories

C = F = IdentifierFactory = NameFactory(
    Identifier, as_sql=lambda self, connection, context: Wildcard()._as_sql(connection, context))

from persistent.mapping import PersistentMapping

from .account import AccountService


class PyRed(PersistentMapping):
    __parent__ = __name__ = None


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = PyRed()
        app_root['accounts'] = AccountService()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']

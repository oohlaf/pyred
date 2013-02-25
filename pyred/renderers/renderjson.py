from pyramid.renderers import JSON
from pyred.models.account import Account


json_renderer = JSON()


def account_adapter(obj, request):
    return {'id': obj.__name__,
            'email': obj.email,
            'created': obj.created.isoformat()}


json_renderer.add_adapter(Account, account_adapter)

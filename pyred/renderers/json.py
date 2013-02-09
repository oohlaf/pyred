from pyramid.renderers import JSON
from pyred.models.account import Account, AccountService


json_renderer = JSON()


def account_adapter(obj, request):
    return {'id': obj.__name__,
            'email': obj.email
           }


def account_service_adapter(obj, request):
    return {'account': [ obj.items(), ] }


json_renderer.add_adapter(Account, account_adapter)
json_renderer.add_adapter(AccountService, account_service_adapter)


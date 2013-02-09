from pyramid.view import view_config
from .models import PyRed
from .models.account import Account, AccountService


@view_config(request_method='POST',
        context=AccountService,
        renderer='json')
def add_account(context, request):
    email = request.params['email']
    password = request.params['password']
    account = Account(email, password)
    return context.add_account(account)


@view_config(request_method='GET',
        context=Account,
        renderer='json')
def view_account(context, request):
    return context


@view_config(request_method='GET',
        context=AccountService,
        renderer='json')
def list_accounts(context, request):
    accounts = context.list_accounts()
    return {'account': list(x[1] for x in accounts)}


@view_config(request_method='GET',
        context=PyRed,
        renderer='templates/application.pt')
def default_view(context, request):
    return {}

import colander

from pyramid.view import view_config
from .models import PyRed
from .models.account import Account, AccountService

import pprint
import logging
log = logging.getLogger(__name__)


class AddAccountFormSchema(colander.MappingSchema):
    email = colander.SchemaNode(colander.String(), validator=colander.Email())
    new_password = colander.SchemaNode(colander.String())
    validate_password = colander.SchemaNode(colander.String())


class AddAccountSchema(colander.MappingSchema):
    account = AddAccountFormSchema()


class ValidationFailure(Exception):
    def __init__(self, msg):
        self.msg = msg


@view_config(context=ValidationFailure,
        renderer='json')
def failed_validation(exc, request):
    request.response.status_int = 422
    return exc.msg


@view_config(request_method='POST',
        context=AccountService,
        renderer='json')
def add_account(context, request):
    schema = AddAccountSchema()
    log.debug('add_account json_body: %s', pprint.pformat(request.json_body))
    try:
        data = schema.deserialize(request.json_body)
    except colander.Invalid, e:
        errors = e.asdict()
        log.debug('add_account errors: %s', pprint.pformat(errors))
        raise ValidationFailure({'errors': errors})
    account = context.add_account(Account(data['account']['email'],
                                          data['account']['new_password']))
    json_map = {'account': account}
    log.debug('add_account info: %r', json_map)
    return json_map


@view_config(request_method='GET',
        context=Account,
        renderer='json')
def view_account(context, request):
    return {'account': context }


@view_config(request_method='GET',
        context=AccountService,
        renderer='json')
def list_accounts(context, request):
    accounts = context.list_accounts()
    return {'accounts': list(x[1] for x in accounts)}


@view_config(request_method='GET',
        context=PyRed,
        renderer='templates/application.pt')
def default_view(context, request):
    return {}

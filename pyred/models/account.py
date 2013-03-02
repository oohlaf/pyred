import cryptacular.core
import cryptacular.bcrypt
import cryptacular.pbkdf2
import hashlib
import logging

from datetime import datetime
from persistent import Persistent
from repoze.folder import Folder


log = logging.getLogger(__name__)


bcrypt = cryptacular.bcrypt.BCRYPTPasswordManager()
pbkdf2 = cryptacular.pbkdf2.PBKDF2PasswordManager()
password_manager = cryptacular.core.DelegatingPasswordManager(
        preferred=bcrypt,
        fallbacks=(pbkdf2,))


def hash_password(password):
    return password_manager.encode(password.encode('utf-8'))


def hash_email(email):
    return hashlib.sha1(email).hexdigest()


class Account(Persistent):
    __name__ = None
    __parent__ = None

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.created = datetime.now()

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)

    def validate_password(self, password):
        return hash_password(password) == self.password

    def __repr__(self):
        return '<%s.%s(email=%s, password=%s) object at 0x%x>' % (
                self.__module__,
                self.__class__.__name__,
                self.email,
                self.password,
                id(self))


class AccountService(Folder):
    __name__ = None
    __parent__ = None

    def __init__(self):
        super(AccountService, self).__init__()

    def add_account(self, account):
        key = hash_email(account.email)
        account.__parent__ = self
        account.__name__ = key
        self[key] = account
        log.debug('Added account %r with key %s' % (account, key))
        return account

    #def remove(self, account_or_key): # check using providedBy with an
    #interface, see
    # http://nullege.com/codes/show/src@r@e@repoze.annotea-0.1@repoze@annotea@models.py/32/repoze.folder.Folder
    def remove_account(self, key):
        del self[key]

    def list_accounts(self):
        return self.items()

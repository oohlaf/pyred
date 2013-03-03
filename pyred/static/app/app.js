/*
 * Application
 */

App = Ember.Application.create({
    LOG_TRANSITIONS: true
});

//Ember.LOG_BINDINGS = true;

/*
 * Models
 */

App.Store = DS.Store.extend({
    revision: 11
});

App.Account = DS.Model.extend({
    firstName: DS.attr('string'),
    lastName: DS.attr('string'),
    email: DS.attr('string'),
    newPassword: DS.attr('string'),
    validatePassword: DS.attr('string'),
    created: DS.attr('date'),

    fullName: function() {
        return this.get('firstName') + ' ' + this.get('lastName');
    }.property('firstName', 'lastName'),
    mailtoEmail: function() {
        return "mailto:" + this.get('email');
    }.property('email')
});

/*
 * Objects
 */

/*
 * Views
 */

App.NavDropdownView = Ember.View.extend({
    classNames: ['dropdown-toggle'],
    tagName: 'a',
    attributeBindings: ['data-toggle'],
    'data-toggle': 'dropdown',
    didInsertElement: function() {
        this.$('.dropdown-toggle').dropdown();
    }
});

/*
 * Controllers
 */

App.AccountsIndexController = Ember.ArrayController.extend();

/*
 * Routing
 */

App.Router.map(function() {
    this.resource('accounts', { path: '/accounts' }, function() {
        this.route('new');
    });
    this.resource('account', { path: '/accounts/:account_id' }, function() {
        this.route('edit');
    });
});

App.AccountsIndexRoute = Ember.Route.extend({
    model: function() {
        return App.Account.find();
    },
    renderTemplate: function() {
        this.render('accounts.index', {
            into: 'application'
        });
    }
});

App.AccountsNewRoute = Ember.Route.extend({
    model: function() {
        var transaction = this.get('store').transaction();
        this.set('transaction', transaction);
        return transaction.createRecord(App.Account, {});
    },
    deactivate: function() {
        this.get('transaction').rollback();
    },
    events: {
        save: function(account) {
            account.one('didCreate', this, function() {
                this.transitionTo('index');
            });
            account.get('transaction').commit();
        }
    },
    renderTemplate: function() {
        this.render('accounts.new', {
            into: 'application'
        });
    }
});

App.AccountIndexRoute = Ember.Route.extend({
    model: function() {
        return this.modelFor('account');
    },
    renderTemplate: function() {
        this.render('account.index', {
            into: 'application'
        });
    }
});

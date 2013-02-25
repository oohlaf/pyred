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
    email: DS.attr('string'),
    newPassword: DS.attr('string'),
    validatePassword: DS.attr('string'),
    created: DS.attr('date')
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
        return App.Account.createRecord();
    },
    events: {
        save: function(account) {
            account.one('didCreate', function() {
                this.replaceWith('accounts.index', account);
            }, this);
            this.get('store').commit();
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

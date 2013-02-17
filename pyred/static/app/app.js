/*
 * Application
 */

Ember.TEMPLATES = window.JST;
App = Ember.Application.create({
    LOG_TRANSITIONS: true
});

/*
 * Models
 */

App.Store = DS.Store.extend({
    revision: 11
});

App.Account = DS.Model.extend({
    email: DS.attr('string')
});

/*
 * Objects
 */

/*
 * Views
 */

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

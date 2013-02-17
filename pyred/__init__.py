from pyramid.config import Configurator
from pyramid.path import AssetResolver
from pyramid_zodbconn import get_connection
from pyramid_webassets import includeme, get_webassets_env
from webassets import Bundle
from .models import appmaker
from .renderers.json import json_renderer


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=root_factory, settings=settings)

    includeme(config)
    jsengine = Bundle('app/vendor/jquery-1.8.2.js',
            'app/vendor/handlebars-1.0.0-rc.3.js',
            'app/vendor/ember-1.0.0-rc.1.js',
            'app/vendor/ember-data.js',
            filters='rjsmin',
            output='js/main.js', debug=False)
    templates = Bundle('app/templates/*.handlebars',
            'app/templates/*/*.handlebars',
            filters='jst',
            output='js/templates.js', debug=False)
    jsapp = Bundle('app/app.js',
            filters='rjsmin',
            output='js/app.js', debug=True)
    config.add_webasset('jsengine', jsengine)
    config.add_webasset('templates', templates)
    config.add_webasset('jsapp', jsapp)

    config.add_renderer('json', json_renderer)

    resolver = AssetResolver()
    static_path = resolver.resolve('pyred:static').abspath()
    config.add_static_view(name='static', path=static_path, cache_max_age=3600)

    config.scan()
    return config.make_wsgi_app()

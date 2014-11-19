#!/usr/env python
# -*- coding: utf-8 -*-

from wscacicneo import config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config.setup(settings)
    from wscacicneo.security import groupfinder
    from wscacicneo.config import routing
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret',
        callback=groupfinder,
        hashalg='sha512',
        include_ip=True,
        timeout=14400
    )
    authz_policy = ACLAuthorizationPolicy()
    cfg = Configurator(settings=settings, root_factory='wscacicneo.models.RootFactory')
    cfg.set_authentication_policy(authn_policy)
    cfg.set_authorization_policy(authz_policy)
    cfg.include('pyramid_chameleon')

    routing.make_routes(cfg)
    cfg.scan()

    return cfg.make_wsgi_app()

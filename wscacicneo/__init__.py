#!/usr/env python
# -*- coding: utf-8 -*-

from wscacicneo import config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound
from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config.setup(settings)
    from wscacicneo.security import groupfinder

    authn_policy = AuthTktAuthenticationPolicy(
        '51f32a7f9359b94b085e145a6951cfe9',
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

    # Session configuration
    cfg.include('pyramid_beaker')
    my_session_factory = SignedCookieSessionFactory(settings['session.secret'],
                                                    cookie_name='session',
                                                    timeout=14400,
                                                    hashalg='sha512',
                                                    reissue_time=0,
                                                    max_age=None,
                                                    path='/',
                                                    domain=None,
                                                    secure=False,
                                                    httponly=False,
                                                    set_on_exception=True,
                                                    salt='pyramid.session.',
                                                    serializer=None
                                                    )
    cfg.set_session_factory(my_session_factory)

    from wscacicneo.config import routing

    routing.make_routes(cfg)
    cfg.scan()

    return cfg.make_wsgi_app()

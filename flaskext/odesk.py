from __future__ import absolute_import
from functools import wraps
from flask import Flask, Module, request, redirect, session, flash, url_for, current_app
from odesk import Client


ODESK_REQUEST_TOKEN = '_ort'
ODESK_ACCESS_TOKEN = '_oat'

odesk = Module(__name__)


def is_authorized():
    """
    Check authorization for current user
    """
    return session.get(ODESK_ACCESS_TOKEN, False) and True
odesk.is_authorized = is_authorized


@odesk.app_context_processor
def inject_is_authorized():
    """
    Context processor for is_authorized method
    """
    return {'odesk_is_authorized': is_authorized()}


def get_access_token():
    """
    Get current access token and access token secret
    """
    return session.get(ODESK_ACCESS_TOKEN, [None]*2)
odesk.get_access_token = get_access_token


def get_client(*access_token):
    """
    Get oDesk Client instance
    """
    try:
        key = current_app.config['ODESK_KEY']
        secret = current_app.config['ODESK_SECRET']
    except KeyError:
        raise Exception("ODESK_KEY and ODESK_SECRET were not found in app.config")
    c = Client(key, secret, auth='oauth')
    if access_token:
        c.oauth_access_token, c.oauth_access_token_secret = access_token
    elif ODESK_ACCESS_TOKEN in session:
        c.oauth_access_token, c.oauth_access_token_secret = session[ODESK_ACCESS_TOKEN]
    return c
odesk.get_client = get_client


def login_required(f):
    """
    Decorator for checking current user authorization
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if ODESK_ACCESS_TOKEN in session:
            return f(*args, **kwargs)
        return login(next=request.url)
    return decorated
odesk.login_required = login_required


@odesk.route('/login')
def login(next=None):
    """
    Start authorization process
    """
    c = get_client()
    session[ODESK_REQUEST_TOKEN] = c.auth.get_request_token()
    return redirect(c.auth.get_authorize_url(url_for('odesk.complete', next=request.args.get('next', next), _external=True)))
odesk.login = login


@odesk.route('/complete')
def complete():
    """
    End authorization process
    """
    c = get_client()
    c.auth.request_token, c.auth.request_token_secret = session[ODESK_REQUEST_TOKEN]
    if ODESK_REQUEST_TOKEN in session:
        del session[ODESK_REQUEST_TOKEN]
    verifier = request.args.get('oauth_verifier')
    access_token = c.auth.get_access_token(verifier)
    authteams = current_app.config.get('ODESK_AUTH_TEAMS', ())
    if authteams:
        c.oauth_access_token, c.oauth_access_token_secret = access_token
        userteams = set(team['id'] for team in c.hr.get_teams())
        if not userteams.intersection(authteams):
            return "Access for your team is denied"
    session[ODESK_ACCESS_TOKEN] = access_token
    flash("You were successfully logged in")
    return redirect(request.args.get('next', '/'))


def log_out():
    """
    Delete oDesk session and log out current user
    """
    if ODESK_ACCESS_TOKEN in session:
        del session[ODESK_ACCESS_TOKEN]
odesk.logout = log_out


@odesk.route('/logout')
def logout():
    """
    Log out current user and redirect it to the next page
    """
    log_out()
    return redirect(request.args.get('next', '/'))

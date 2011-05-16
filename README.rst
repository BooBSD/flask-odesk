===========
Flask-oDesk
===========

Requirements
============

    * `flask`
    * `python-odesk`
    * `python-oauth2`


Authorization
==============

Quick start
-----------

Before you may use oDesk APIs, you will need to obtain your pair of API keys.
Visit the `oDesk API Center documentation <http://developers.odesk.com/Authentication#authentication>`_
for full details. Please note, that Flask-oDesk uses authorization via OAuth and it needs keys with auth type "OAuth".

Please make sure, that `SECRET_KEY` which is necessary for sessions, based on the secure cookies, is indicated in `settings.py`:: 

    SECRET_KEY = '(your random secret key)'

You need to store your pair of oDesk API keys in `settings.py`::

    ODESK_KEY = '(your oDesk public key)'
    ODESK_SECRET = '(your oDesk secret key)'

You can also set the list of teams in `settings.py`, which will be able to authorize.
If you do not specify this option or leave the list empty, then all oDesk users will be able to authorize::


    ODESK_AUTH_TEAMS = ('odesk:odeskpsbootcamp',)

Please make sure, that you have registered odesk module in your `app.py` correctly.
Please keep in mind, that `url_prefix` can be whatever you like::

    from flask import Flask
    from flaskext.odesk import odesk

    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    app.register_module(odesk, url_prefix='/odesk')



Using authorization
-------------------

Please use the decorator `login_required` to close the access for anonymous users to the certain parts of your website::

    @app.route('/only/for/odesk/users')
    @odesk.login_required
    def admin():
        return "Welcome, oDesk user!"

If you want to indicate login or logout links in the template, than you can use `url_for` function::

    <a href="{{ url_for('odesk.login') }}">oDesk log in</a>
    <a href="{{ url_for('odesk.logout') }}">oDesk log out</a>

To check the authorization of the current user you can use `is_authorized` method::

    @app.route('/test')
    def test():
        if odesk.is_authorized():
            return "You are authorized."
        else:
            return "You are not authorized yet."

If you need, you can start the authorization process manually from your code::

    if not odesk.is_authorized():
        return odesk.login()

You can also use `next` parameter to indicate URL, where will be redirect after the authorization process ends::

    if not odesk.is_authorized():
        return odesk.login(next='/blah/blah')

You can use `logout` method for user's logging out.
Please pay attention, that unlike `login` this method do not return the bulk of redirects.
It simply deletes the OAuth session. You should return response manually::

    if odesk.is_authorized():
        odesk.logout()
        return redirect('/')


Using client
============

You can use `get_access_token` method to get the current access token and access token secret,
that can be stored in DB and used for access to the client later, if necessary::

    if odesk.is_authorized():
        access_token, access_token_secret = odesk.get_access_token()

You can use `get_client` method to get the client::

    if odesk.is_authorized():
        c = odesk.get_client()
        c.team.get_teamrooms()

Or you can use the client even if the current user is not authorized,
but you have the access token and access token secret::

    if not odesk.is_authorized():
        c = odesk.get_client(access_token, access_token_secret)
        c.team.get_teamrooms()

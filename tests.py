from flask import Flask, url_for
from flaskext.odesk import odesk
from mock import patch
import unittest


class ODeskTestCase(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'blahblah'
        app.config['ODESK_KEY'] = '56adf4b66aaf61444a77796c17c0da53'
        app.config['ODESK_SECRET'] = 'e5864a0bcbed2085'
        app.register_module(odesk, url_prefix='/odesk')
        ctx = app.test_request_context()
        ctx.push()
        self.app = app
        self.tc = self.app.test_client()


    def test_url_for(self):
        assert url_for('odesk.login') == '/odesk/login'
        assert url_for('odesk.logout') == '/odesk/logout'


    def test_login_required(self):

        def patched_httplib2_request(*args, **kwargs):
            return {'status': '200'}, 'oauth_callback_confirmed=1&oauth_token=709d434e6b37a25c50e95b0e57d24c46&oauth_token_secret=193ef27f57ab4e37'

        def patched_httplib2_access(*args, **kwargs):
            return {'status': '200'}, 'oauth_token=aedec833d41732a584d1a5b4959f9cd6&oauth_token_secret=9d9cccb363d2b13e'

        def patched_get_authorize_url(*args, **kwargs):
            return url_for('odesk.complete', next='/admin', oauth_verifier='590b901a040d76453da588bf5a8601e9')

        @self.app.route('/admin')
        @patch('httplib2.Http.request', patched_httplib2_request)
        @patch('odesk.oauth.OAuth.get_authorize_url', patched_get_authorize_url)
        @patch('httplib2.Http.request', patched_httplib2_access)
        @odesk.login_required
        def admin():
            self.odesk_is_authorized = odesk.is_authorized()
            odesk.logout()
            self.odesk_is_not_authorized = odesk.is_authorized()
            return "Welcome, oDesk user!"

        response = self.tc.get('/admin', follow_redirects=True)
        assert "Welcome" in response.data
        assert self.odesk_is_authorized == True
        assert self.odesk_is_not_authorized == False


if __name__ == '__main__':
    unittest.main()

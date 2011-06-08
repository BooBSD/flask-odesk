from flask import Flask, render_template, session
from flaskext.odesk import odesk


app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.register_module(odesk, url_prefix='/odesk')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/team')
@odesk.login_required
def team():
    c = odesk.get_client()
    teamrooms = c.team.get_teamrooms_2()
    teams = [t for t in teamrooms if not t.update({'snapshots': c.team.get_snapshots_2(t.get('id'), online='all')})]
    return render_template('team.html', teams=teams)


@odesk.after_login
def save_user_session():
    u = odesk.get_client().hr.get_user('me')
    session['user'] = {
        'name': u'%s %s' % (u.get('first_name'), u.get('last_name')),
        'url': u.get('public_url'),
    }


@odesk.after_logout
def delete_user_session():
    if 'user' in session:
        del session['user']


app.run()

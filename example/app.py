from flask import Flask, render_template
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


app.run()

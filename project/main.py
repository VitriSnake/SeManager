from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from .models import User
import json
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def join():
    with open('./team.json', 'r') as team_file:
        team_data = json.load(team_file)
    if team_data['setup'] == False:
        return redirect('/setup')
    else:
        return redirect('/app')

@main.route('/app')
@login_required
def index():
        user = User.query.filter_by(name=current_user.name).first()
        return render_template('index.html', user=current_user.name, teamname="SeManager", rank=user.rank)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
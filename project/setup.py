from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from .models import User
import time
import json
from . import db

with open('./team.json', 'r') as team_file:
    team_data = json.load(team_file)

app_setup = Blueprint('setup', __name__)

setup_dict = {"setup": True}

@app_setup.route('/setup')
def setup():
    return redirect('/setup/step1')

# Step 1
@app_setup.route('/setup/step1')
def setup1():
    return render_template('team_config.html')

@app_setup.route('/setup/step1/form', methods=['POST'])
def setup1_form():
    teamname = request.form.get('team')
    admin_password = request.form.get('password')
    admin_user = request.form.get('user')
    admin_email = request.form.get('email')

    data = {"setup": True, "team": teamname}

    with open('./team.json', 'w') as team_file:
        team_data = json.dump(data, team_file)

    return "GREAT!"
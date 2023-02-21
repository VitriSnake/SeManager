from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .models import Team
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
    password = request.form.get('password')
    user = request.form.get('user')
    email = request.form.get('email')

    print(user)

    data = {"setup": True}

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    team = Team(name=teamname)

    # add the new user to the database
    db.session.add(team)
    db.session.commit()

    with open('./team.json', 'w') as team_file:
        team_data = json.dumps(data)
        team_file.write(team_data)
    team_file.close()

    user_e = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user_e: # if a user is found, we want to redirect back to signup page so user can try again
        return "E: User exsists. Please reinstall your application or report it on GitHub"

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=user, password=generate_password_hash(password, method='sha256'), rank="Admin", manager="1")

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect('/app')
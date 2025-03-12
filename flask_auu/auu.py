# last change 11 March 23

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flask_auu.auth import login_required
from flask_auu.db import get_db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():

    #document the session
    session['history'] = session['history'] + "/index\n ... "
    flash(session['history'])

    return render_template('index.html',)

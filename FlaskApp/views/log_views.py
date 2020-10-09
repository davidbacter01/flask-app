from flask import Blueprint, redirect, render_template, request
from services.services import Services


log_views_blueprint = Blueprint('log_views', __name__)

@log_views_blueprint.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method == 'GET':
        return render_template('login.html')

    #return redirect('/login')

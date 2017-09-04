from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from uuid import uuid1
from . import console
from .forms import APIKeyForm
# from ..models import APIKey, User
from sharedmodels.models import APIKey, User
from .. import db


@console.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('console/dashboard.html')


@console.route('/doc/detect', methods=['GET'])
@login_required
def detect():
    return render_template('console/api/detect.html')


@console.route('/doc/faceset_create', methods=['GET'])
@login_required
def faceset_create():
    return render_template('console/api/faceset/create.html')


@console.route('/apikey/create', methods=['GET', 'POST'])
@login_required
def apikey_create():
    form = APIKeyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if user is not None:
            apikey = APIKey(application=form.application.data,
                            apikey=str(uuid1()), user=user)
            db.session.add(apikey)
            db.session.commit()
        return redirect(url_for('.apikey_list'))
    return render_template('console/apikey/create.html', form=form)


@console.route('/apikey/list', methods=['GET'])
@login_required
def apikey_list():
    user = current_user
    api_keys = []
    if user is not None:
        api_keys = []
        api_key_objs = user.api_keys.all()
        for api_key_obj in api_key_objs:
            api_keys.append([api_key_obj.application, api_key_obj.apikey])
    return render_template('console/apikey/list.html',
                           api_keys=api_keys, user=user)


@console.route('/apikey/view/<api_key>')
@login_required
def apikey_view(api_key):
    user = current_user
    apikey = user.api_keys.filter_by(apikey=api_key).first()
    if apikey is None:
        return redirect(url_for('.apikey_list'))
    return render_template('console/apikey/view.html', apikey=apikey)

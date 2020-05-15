from flask import render_template, redirect, url_for, flash
from rad_apps import app, app_list, queue
from .tasks import app_wrapper
from .forms import ChooseApp, get_form


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ChooseApp()
    if form.validate_on_submit():
        app_name = form.app_name.data
        return redirect(url_for('input', app_name=app_name))
    return render_template('index.html', form=form)


@app.route('/apps/<app_name>', methods=['GET', 'POST'])
def input(app_name):
    form = get_form(app_name)
    long_name = app_list.get_app_info(app_name).long_name
    if form.validate_on_submit():
        queue.enqueue(app_wrapper, app_name, form.data, job_timeout=3600)
        flash(f'Analysis request submitted for acc # {form.acc.data}')
        form.acc.data = ''
        return render_template('input.html', title=app_name, long_name=long_name, form=form)
    return render_template('input.html', title=app_name, long_name=long_name, form=form)

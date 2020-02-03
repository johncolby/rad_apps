from flask import request, render_template, redirect, url_for, flash
from rad_apps import app, queue
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
    if form.validate_on_submit():
        queue.enqueue(app_wrapper, app_name, form.data, job_timeout=2700)
        flash(f'Analysis request submitted for acc # {form.acc.data}')
        form.acc.data = ''
        return render_template('input.html', form=form)
    return render_template('input.html', form=form)
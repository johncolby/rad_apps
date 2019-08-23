from flask import request, render_template, redirect, url_for, flash
from app import app, queue
from app.tasks import process_gbm_wrapper
from app.forms import SegmentationForm

@app.route('/', methods=['GET', 'POST'])
def main():
    email = request.args.get('email') or ''
    form = SegmentationForm(email=email)
    if form.validate_on_submit():
        queue.enqueue(process_gbm_wrapper, form.data, job_timeout=2700)
        flash(f'Segmentation request submitted for acc # {form.acc.data}')
        return redirect(url_for('main', email=form.email.data))
    return render_template('input.html', form=form)
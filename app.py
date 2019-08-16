from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('input.html')
    if request.method == 'POST':
        return render_template('result.html', acc=request.form['acc'])
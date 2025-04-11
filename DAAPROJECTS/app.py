from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run/<algorithm>')
def run_algorithm(algorithm):
    subprocess.Popen(["python", "pathfinding.py", algorithm])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

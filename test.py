from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'Missing files'})
    file1 = request.files['file1']
    file2 = request.files['file2']
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    # Call your genetic algorithm function here with df1 and df2
    # and get the output as a dictionary
    output = {'result': 'some output'}
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)

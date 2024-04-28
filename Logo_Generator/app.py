import os
from flask import Flask,  request, jsonify, send_from_directory
import test
from gen_data import gen_data
from flask_cors import CORS
from options import get_parser
import sys 
from io import StringIO


app = Flask(__name__)
CORS(app)
parser = get_parser()
opts = parser.parse_args()

class RedirectStdout:
    def __init__(self):
        self.buffer = StringIO()

    def write(self, output):
        self.buffer.write(output)

    def flush(self):
        pass

redirect_stdout = RedirectStdout()
sys.stdout = redirect_stdout

@app.route('/api/output', methods=['GET'])
def get_output():
    output = redirect_stdout.buffer.getvalue()
    redirect_stdout.buffer.seek(0)
    redirect_stdout.buffer.truncate(0)
    return jsonify({'output': output})


@app.route("/api/create", methods=['POST'])
def use_model():
    word = request.json
    print(word)
    print(type(word))
    opts.mode = 'test'
    opts.input_text = word
    # opts.style = 'texture_style/test2-paint.png'
    # opts.style_sem = 'texture_style/test2-sem.png'
    opts.style = 'texture_style/glyh-paint.png'
    opts.style_sem = 'texture_style/glyh-sem.png'
    opts.experiment_name = opts.experiment_name
    gen_data(opts)
    print(f"Testing on experiment {opts.experiment_name}...")
    test.test(opts)
    return jsonify({"message": "successful cycle"}), 200


@app.route("/api/results/<filename>", methods=['GET'])
def get_result(filename):
    try:
        return send_from_directory("./outputs", filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "Image not found"}), 404
    
@app.route("/api/logo/<filename>", methods=['GET'])
def get_logo(filename):
    try:
        return send_from_directory("./texture_style/YourDataSet/", filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "Image not found"}), 404
@app.route("/api/upload",methods=["POST"])
def upload_texture():
    uploaded_files = request.files.getlist('texture[]')
    for file in uploaded_files:
        if file:
            # Save the file to a desired location
            file.save(f'texture_style/{file.filename}')
    return jsonify({'message': 'Files uploaded successfully'})
if __name__ == "__main__":
    app.run(debug=True, port=8000)

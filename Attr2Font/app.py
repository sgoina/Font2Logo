# built-in imports
import os
import re

# third party imports
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from dotenv import load_dotenv

# local imports
import main
from options import get_parser
from utils import get_font_folder_names, update_file_except_png_numbers, get_last_prefix,create_attribute_picture

# initialize the app
load_dotenv()
app = Flask(__name__)
CORS(app)
parser = get_parser()
opts = parser.parse_args()
opts.unsuper_num = 968
ATTRIBUTES = os.getenv('ATTRIBUTES_FILE')
RESULT_DIR = "./experiments/att2font_en/results"
ATTRIBUTES_DIR = "./data/explor_all/" + ATTRIBUTES
IMAGE_PATH = "data/explor_all/image"


def parse_attributes_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Assuming the first line contains attribute names
    attribute_names = lines[0].strip().split()
    data = {}
    for line in lines[1:]:
        parts = line.strip().split()
        filename = parts[0]
        attribute_values = list(map(int, parts[1:]))
        data[filename] = attribute_values
    return attribute_names, data


@app.route('/api/image/B', methods=['GET'])
def get_imageB():
    return jsonify({"data": get_last_prefix(ATTRIBUTES_DIR)})
# this gets images from result folder


@app.route('/api/image/<filename>', methods=['GET'])
def get_image(filename):
    try:
        return send_from_directory(RESULT_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "Image not found"}), 404


@app.route("/api/", methods=["GET"])
def test_model():
    opts.phase = 'test'
    opts.test_epoch = 30
    main.test(opts)
    return jsonify({"message": "successful cycle"}), 200


@app.route('/results/<filename>')
def results(filename):
    return send_from_directory(RESULT_DIR, filename)

@app.route("/api/attr/<filename>", methods=['GET'])
def get_logo(filename):
    try:
        return send_from_directory("./experiments/att2font_en/results/", filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "Image not found"}), 404
    
@app.route('/api/attributes/<prefix>', methods=['GET'])
def get_attributes(prefix):

    if not prefix.endswith('/'):
        prefix += '/'
    attribute_names, data = parse_attributes_file(
        ATTRIBUTES_DIR)
    result = []

    for filename, attribute_values in data.items():
        if filename.startswith(prefix):
            result.append({
                "filename": filename,
                "attributes": dict(zip(attribute_names, attribute_values))
            })

    if not result:
        return jsonify({"error": "No data found for the given prefix"}), 404

    return jsonify({"data": result})


@app.route('/api/attributes/<prefix>', methods=['POST'])
def update_attributes(prefix):
    # attribute_values = request.json 
    # print(attribute_values)
    # print(prefix)
    if not prefix.endswith('/'):
        prefix += '/'
    # Read 37 attributes from the request body
    attribute_values = request.json
    if not attribute_values or len(attribute_values) != 37:
        return jsonify({"error": "Exactly 37 attributes required"}), 400
    # Parse the existing attributes file
    attribute_names, data = parse_attributes_file(
        ATTRIBUTES_DIR)

    # Update the attributes of the prefix filename
    updated = False
    for filename, values in data.items():
        if filename.startswith(prefix):
            data[filename] = attribute_values
            updated = True

    # If the filename with the prefix was not found, return an error
    if not updated:
        return jsonify({"error": "Filename with the given prefix not found"}), 404

    # Write the updated attributes back to the file
    with open(ATTRIBUTES_DIR, 'w') as file:
        file.write(' '.join(attribute_names) + '\n')
        for filename, values in data.items():
            file.write(filename + ' ' + ' '.join(map(str, values)) + '\n')

    return jsonify({"message": "Attributes updated successfully"}), 200


@app.route('/api/image', methods=['POST'])
def change_image():
    files = request.json
    update_file_except_png_numbers(
        ATTRIBUTES_DIR, files.get('imageA'), files.get('imageB'))
    return jsonify({"message": "Image updated successfully"}), 200


@app.route('/api/list', methods=['GET'])
def listarray():
    font_folder_names = get_font_folder_names(IMAGE_PATH)
    return jsonify({"data": font_folder_names})
@app.route('/api/saveattr',methods=['POST'])
def save_attr_pic():
    files = request.json
    create_attribute_picture(opts=opts,switch=files.get('switch'))
    return jsonify({"message": "attr img saved"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)

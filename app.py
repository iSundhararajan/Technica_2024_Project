from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
from flask_cors import CORS
import hashlib



app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def uploadFile():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file: 
        file_hash = generate_hash(file)
        return jsonify("Generating hash...")
  
    
def generate_hash(f):
    hasher = hashlib.sha256()

    for chunk in iter(lambda: f.read(4096), b""):
        hasher.update(chunk)

    print('{}: {}'.format(hasher.name, hasher.hexdigest()))
    return hasher.hexdigest()


# Run the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
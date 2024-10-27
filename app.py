from flask import Flask, render_template, jsonify, request, redirect, url_for, send_file
from flask_socketio import SocketIO
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


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
        return "Generating hash..."
    

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
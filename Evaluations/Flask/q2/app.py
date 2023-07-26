import hashlib
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/md5_hash', methods=['POST'])
def generate_md5_hash():
    try:
        if 'file' not in request.files:
            error="No file part"
            return render_template('index.html', error=error)

        file = request.files['file']
        if file.filename == '':
            error="No selected file"
            return render_template('index.html', error=error)

        image_bytes = file.read()
        image_hash = hashlib.md5(image_bytes).hexdigest()
        return render_template('index.html', md5_hash=image_hash)
    except Exception as e:
        return render_template('index.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)
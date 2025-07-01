from flask import Flask, request, jsonify, send_from_directory
import os
from services.smell_detection import SmellDetector

app = Flask(__name__)
detector = SmellDetector()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("frontend", filename)

@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_files = request.files.getlist("file")
    results = []

    for file in uploaded_files:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        smells = (
            detector.detect_long_parameter_list(filepath) +
            detector.detect_long_method(filepath) +
            detector.detect_large_class(filepath) +
            detector.detect_data_class(filepath) +
            detector.detect_lazy_class(filepath) +
            detector.detect_magic_numbers(filepath)
        )

        results.extend([smell.to_dict() for smell in smells])

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)

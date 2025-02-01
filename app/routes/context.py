from flask import Blueprint, request, render_template, jsonify, Response, stream_with_context
import os
import json
from app.utils import extract_ueba_from_evtx, update_context_file
from werkzeug.utils import secure_filename
from Evtx.Evtx import Evtx

context_bp = Blueprint('ueba', __name__)

CONTEXT_FILE = 'context.json'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@context_bp.route('/', methods=['GET'])
def manage_context():
    """Displays the current UEBA context."""
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
            context_data = json.load(f)
    else:
        context_data = {}

    return render_template('context.html', context_data=context_data)

@context_bp.route('/upload_progress', methods=['POST'])
def upload_progress():
    """Handles EVTX file upload and streams progress updates."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(file_path)

    def process_evtx():
        """Processes EVTX file and streams remaining registry count."""
        with Evtx(file_path) as evtx_log:
            total_entries = sum(1 for _ in evtx_log.records())  # Count total lines
            remaining_entries = total_entries

            yield f"data: {total_entries}\n\n"  # Send total count first
            extracted_data = extract_ueba_from_evtx(file_path)

            for index, _ in enumerate(extracted_data.items()):
                remaining_entries -= 1
                yield f"data: {remaining_entries}\n\n"  # Send progress update
                import time
                time.sleep(0.05)  # Simulate delay for better visibility

            update_context_file(extracted_data)
            yield "data: Upload Complete!\n\n"

    return Response(stream_with_context(process_evtx()), mimetype='text/event-stream')

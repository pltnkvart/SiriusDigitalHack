from flask import Blueprint, request, jsonify, session

from server.session_manager import create_session, add_file_to_session
from utils.parser import convert_xlsx_to_json
import tempfile

bp = Blueprint('upload', __name__)


@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    session_id = create_session()
    session['upload_id'] = session_id

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_input_file:
        input_xlsx_file = temp_input_file.name
        file.save(input_xlsx_file)

        json_files = tempfile.NamedTemporaryFile(delete=False, suffix='.json')

        convert_xlsx_to_json(input_xlsx_file, json_files.name)

        file_id = add_file_to_session(session_id, json_files.name)

    return jsonify({
        "message": "File uploaded successfully",
        "session_id": session_id,
        "result_id": file_id,
    }), 200

from flask import Blueprint, request, jsonify, session, send_file
import tempfile

from utils.parser import convert_xlsx_to_json
from utils.session_manager import create_session, add_file_to_session, get_file_for_session

bp = Blueprint('files', __name__)


@bp.route('/files/upload', methods=['POST'])
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

        add_file_to_session(session_id, json_files.name)

    return send_file(json_files.name, as_attachment=True)


@bp.route('/files/download/', methods=['GET'])
def download_file():
    session_id = session.get('upload_id')
    if not session_id:
        return jsonify({"error": "No active session or invalid session ID"}), 400

    try:
        file_path = get_file_for_session(session_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return send_file(file_path, as_attachment=True)

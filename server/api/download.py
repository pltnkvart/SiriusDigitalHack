from flask import Blueprint, jsonify, send_file, session
from server.session_manager import get_file_for_session

bp = Blueprint('download', __name__)


@bp.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    session_id = session.get('upload_id')
    if not session_id:
        return jsonify({"error": "No active session or invalid session ID"}), 400

    try:
        file_path = get_file_for_session(session_id, file_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return send_file(file_path, as_attachment=True)

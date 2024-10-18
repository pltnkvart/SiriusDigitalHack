from flask import Blueprint, session, jsonify, request

from utils.exchange import exchange_words
from utils.session_manager import get_file_for_session

bp = Blueprint('change_value', __name__)


@bp.route('/change_values/<file_id>', methods=['POST'])
def download_file(file_id):
    session_id = session.get('upload_id')

    if not session_id:
        return jsonify({"error": "No active session or invalid session ID"}), 400

    input_data = request.json

    if 'question_name' not in input_data.keys():
        return jsonify({"error": "No question name"}), 400

    if 'word_before_change' not in input_data.keys():
        return jsonify({"error": "No word being changed"}), 400

    if 'word_after_change' not in input_data.keys():
        return jsonify({"error": "No word after change"}), 400

    word_before_change = input_data['word_before_change']
    word_after_change = input_data['word_after_change']
    question_name = input_data['question_name']

    try:
        file_path = get_file_for_session(session_id, file_id)
        exchange_words(file_path, question_name, word_before_change, word_after_change, full_entry=False)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "message": "Values changed successfully",
        "session_id": session_id,
    }), 200

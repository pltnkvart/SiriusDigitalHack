from flask import Blueprint, session, jsonify, request
import json

from utils.session_manager import get_file_for_session

bp = Blueprint('edit', __name__)


@bp.route('/edit/move-questions', methods=['POST'])
def move_questions():
    content = request.json
    from_group_id = content['from_group_id']
    question_id = content['question_id']

    session_id = session.get('upload_id')
    if not session_id:
        return jsonify({"error": "No active session or invalid session ID"}), 400

    try:
        file_path = get_file_for_session(session_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    try:
        to_group_id = content['to_group_id']
    except KeyError:
        to_group_id = max([group['id'] for group in data['groups']]) + 1

    from_group = next((group for group in data['groups'] if group['id'] == from_group_id), None)
    to_group = next((group for group in data['groups'] if group['id'] == to_group_id), None)

    if from_group is None:
        return jsonify({"error": "From group ID not found."}), 404

    if question_id in from_group['question_ids']:
        from_group['question_ids'].remove(question_id)
        if len(from_group['question_ids']) == 0:
            data['groups'].remove(from_group)
        if to_group is not None:
            to_group['question_ids'].append(question_id)
        else:
            max([group['id'] for group in data['groups']]) + 1
            data['groups'].append({
                "id": to_group_id,
                "question_id": question_id,
            })

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return jsonify({"message": "Questions moved successfully."}), 200

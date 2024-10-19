import json

from flask import Blueprint, jsonify, session
import tempfile
import pickle

from utils.clusters import make_clusterization
from utils.session_manager import get_file_for_session

from backend.utils.clusters import make_clusterization_for_group
from backend.utils.session_manager import add_file_by_session_and_group

bp = Blueprint('clusters', __name__)


@bp.route('/clusters', methods=['GET'])
def generate_clusters():
    try:
        session_id = session.get('upload_id')
        file_path = get_file_for_session(session_id)
        questions_clusters_array = make_clusterization(file_path)

        with open('data.pickle', 'wb') as f:
            pickle.dump(questions_clusters_array, f)


    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(questions_clusters_array), 200

@bp.route('/clusters/<group_id>', methods=['POST'])
def get_group_clusters(group_id):

    try:

        session_id = session.get('upload_id')
        file_path = get_file_for_session(session_id)

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        questions_idxes = []
        for group in data['groups']:
            if group['id'] == group_id:
                questions_idxes = group['question_ids']
                break

        questions = []
        for question in data['questions']:
            if question['id'] in questions_idxes:
                questions.append(question)

        questions_clusters_array = make_clusterization_for_group(questions)
        # todo: save questions_clusters_array to pickle
        # add_file_by_session_and_group(session_id, group_id, <paste here path>)

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

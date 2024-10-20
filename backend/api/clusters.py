import json

from flask import Blueprint, jsonify, session, request
import tempfile
import pickle

from utils.clusters import make_clusterization
from utils.session_manager import get_file_for_session

from utils.clusters import make_clusterization_for_group
from utils.session_manager import add_file_by_session_and_group
from utils.gpt_answer import analyze_word_frequency_gigachat, get_word_frequency_gigachat

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

@bp.route('/clusters/<group_id>', methods=['GET'])
def get_group_clusters(group_id):
    try:
        session_id = session.get('upload_id')
        file_path = get_file_for_session(session_id)

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        questions_idxes = []
        print(f"groups: {data['groups']}")
        for group in data['groups']:
            print(f"id:{group['id']} == group_id:{group_id} --- {str(group['id']) == str(group_id)}")
            if str(group['id']) == str(group_id):
                print(f"group: {group['question_ids']}")
                questions_idxes = list(group['question_ids'])
                break

        print(f"questions_idxes: {questions_idxes}")

        questions = []
        for question in data['questions']:
            print(f"question id: {question}")
            if question['id'] in questions_idxes:
                questions.append(question)

        print(f"questions: {questions}")
        questions_clusters_array = make_clusterization_for_group(questions)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pickle') as temp_file:
            temp_file_name = temp_file.name
            pickle.dump(questions_clusters_array, temp_file)
            add_file_by_session_and_group(session_id, group_id, temp_file_name)

        return jsonify(questions_clusters_array), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/magic', methods=['POST'])
def magic():
    try:
        # Extract data from the incoming POST request
        data = request.get_json()
        question = data.get('question')
        main_points = data.get('mainPoints')

        if not question or not main_points:
            raise ValueError("Invalid input: 'question' and 'mainPoints' are required")

        # Call your analysis function
        questions_clusters_array = analyze_word_frequency_gigachat(question, main_points)

        # Return the successful response
        return jsonify(questions_clusters_array), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500

@bp.route('/magic_points', methods=['POST'])
def magic_points():
    try:
        # Extract data from the incoming POST request
        data = request.get_json()
        main_points = data.get('mainPoints')

        # Call your analysis function
        questions_clusters_array = get_word_frequency_gigachat(main_points)

        # Return the successful response
        return jsonify(questions_clusters_array), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500


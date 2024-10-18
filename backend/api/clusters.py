from flask import Blueprint, jsonify, session

from utils.clusters import make_clusterization
from utils.session_manager import get_file_for_session

bp = Blueprint('clusters', __name__)


@bp.route('/clusters', methods=['GET'])
def download_file(file_id):

    try:
        session_id = session.get('upload_id')
        file_path = get_file_for_session(session_id, file_id)
        questions_clusters_array = make_clusterization(file_path)

        for question in questions_clusters_array:
            print(f"new question")
            for cluster in question:
                print("new cluster")
                for answer in range(min(len(cluster), 2)):
                    print(cluster[answer])

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(questions_clusters_array), 200

from flask import Blueprint, jsonify

bp = Blueprint('greeting', __name__)


@bp.route('/greeting', methods=['GET'])
def download_file():
    return jsonify({"success": "hello world"}), 200

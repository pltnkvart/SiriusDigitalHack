from flask import Blueprint, jsonify

bp = Blueprint('greeting', __name__)


@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "healthy"}), 200

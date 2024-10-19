from flask import Flask
import os
from flask_cors import CORS

from api import files, health, edit, clusters

app = Flask(__name__)
app.json.sort_keys = False
app.secret_key = os.urandom(24)

CORS(app, origins="http://localhost:5173", supports_credentials=True)

app.register_blueprint(health.bp)
app.register_blueprint(files.bp)
app.register_blueprint(edit.bp)
app.register_blueprint(clusters.bp)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5050)

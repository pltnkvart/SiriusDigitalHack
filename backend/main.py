from flask import Flask
import atexit
import os

from api import files, health, change_value, clusters

app = Flask(__name__)
app.json.sort_keys = False
app.secret_key = os.urandom(24)

temporary_files = {}


def cleanup():
    for temp_files in temporary_files.values():
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except OSError:
                print(f"Error removing temporary file: {temp_file}")


atexit.register(cleanup)

app.register_blueprint(health.bp)
app.register_blueprint(files.bp)
app.register_blueprint(change_value.bp)
app.register_blueprint(clusters.bp)

if __name__ == '__main__':
    app.run(debug=True)

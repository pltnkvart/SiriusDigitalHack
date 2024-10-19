import os
import uuid
import atexit

temporary_files = {}


def create_session():
    session_id = str(uuid.uuid4())
    temporary_files[session_id] = None
    return session_id


def add_file_to_session(session_id: str, file_path: str):
    if session_id in temporary_files:
        temporary_files[session_id] = file_path
    else:
        raise ValueError("Invalid session ID")


def get_file_for_session(session_id: str) -> str:
    if session_id in temporary_files:
        if temporary_files[session_id] is not None:
            return temporary_files[session_id]
        else:
            raise ValueError("No file found")
    else:
        raise ValueError("Invalid session ID")


def cleanup():
    for session_id, files in temporary_files.items():
        try:
            os.remove(files)
        except OSError as e:
            print(f"Error removing temporary file: {files} - {e}")

    temporary_files.clear()


atexit.register(cleanup)

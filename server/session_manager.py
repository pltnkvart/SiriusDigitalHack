import os
import uuid
import atexit
import random
import string

temporary_files = {}


def generate_random_id(length=8) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def create_session():
    session_id = str(uuid.uuid4())
    temporary_files[session_id] = {}
    return session_id


def add_file_to_session(session_id: str, file_path: str) -> str:
    if session_id in temporary_files:
        file_id = generate_random_id()
        temporary_files[session_id][file_id] = file_path
        return file_id
    else:
        raise ValueError("Invalid session ID")


def get_file_for_session(session_id: str, file_id: str) -> str:
    if session_id in temporary_files:
        if file_id in temporary_files[session_id]:
            return temporary_files[session_id][file_id]
        else:
            raise ValueError("Invalid file ID")
    else:
        raise ValueError("Invalid session ID")


def cleanup():
    for session_id, files in temporary_files.items():
        for file_path in files.values():
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Error removing temporary file: {file_path} - {e}")

    temporary_files.clear()


atexit.register(cleanup)

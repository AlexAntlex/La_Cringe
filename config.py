import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'La_cringe'
    UPLOAD_FOLDER_USER = 'static/users_files/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_FILE_SIZE = 1024 * 1024 + 1
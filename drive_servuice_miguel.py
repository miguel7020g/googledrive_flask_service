from flask import Flask, request, url_for, jsonify
from drive_manager import DriveManager
from db_manager import DatabaseManageer
from oauth2client import file, client, tools
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'



@app.route('/drive_service', methods=['GET', 'POST'])
def drive_service():
    if request.method == 'POST':
        data = request.get_json()
        media_path = data['media_path']
        drive_path = data['drive_path']
        file_name = data['file_name']
        return DriveManager().load_to_drive_path(media_path, drive_path, file_name)

    else:
        if request.args.get('id', ''):
            id = request.args.get('id', '')
            return DatabaseManageer().file_by_id(id)
        else:
            return DatabaseManageer().full_db_register()

# curl -i -X POST -H 'Content-Type: application/json' -d '{"media_path": "/home/miguel/Pictures/Wallpapers/spacex.jpg", "drive_path": "my_first_upload/sub1/sub2_1", "file_name":"spacex.jpg"}' http://localhost:5000/drive_service

from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
from main import get_video_info, download_audio
import os

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET'])
def info():
    print(request)
    video_url = request.args.get('video_url')
    
    if not video_url:
        return jsonify({'error': 'Missing video url parameter'}), 400

    video_info = get_video_info(video_url)
    return jsonify(video_info)

@app.route('/api', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get('video_url')
    no_play_list = data.get('no_play_list')
    user_cookies = request.cookies.get('user_cookies')
    if not video_url:
        return jsonify({'error': 'Missing video url parameter'}), 400

    file_name = download_audio(video_url, no_play_list=True, cookies = user_cookies)

    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_name)
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
        return response

    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

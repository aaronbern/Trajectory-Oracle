import os
import cv2
from flask import Flask, request, jsonify, send_from_directory, render_template
from process_video import process_video  # Import your process_video function

UPLOAD_FOLDER = './uploaded_videos'
OUTPUT_FOLDER = './output_frames'

app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Route for the root URL, returning a welcome message or basic HTML
@app.route('/')
def index():
    return """
    <h1>Welcome to the Trajectory Oracle App!</h1>
    <p>Use the /process_video endpoint to upload and process a video.</p>
    """

# Route for processing the video
@app.route('/process_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    video_filename = video.filename
    video_path = os.path.join(UPLOAD_FOLDER, video_filename)

    # Save uploaded video
    video.save(video_path)

    # Use the default distance threshold and prediction frames for simplicity
    output_dir = os.path.join(OUTPUT_FOLDER, os.path.splitext(video_filename)[0])
    process_video(video_path, output_dir)  # Call your existing process_video function

    # Send back the processed video URL to the client
    output_video_url = f"/output/{os.path.splitext(video_filename)[0]}/output_with_trajectory.mp4"
    return jsonify({'output_video_url': output_video_url})

# Route for serving the processed video
@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

# Main
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

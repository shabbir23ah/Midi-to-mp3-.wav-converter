import os
import subprocess
from flask import Flask, request, redirect, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['mid_file']
    if file and file.filename.endswith('.mid'):
        input_path = os.path.join(os.getcwd(), file.filename)
        wav_output_path = os.path.join(os.path.expanduser('~'), 'Music', file.filename.replace('.mid', '.wav'))
        mp3_output_path = os.path.join(os.path.expanduser('~'), 'Music', file.filename.replace('.mid', '.mp3'))

        file.save(input_path)

        # Convert .mid to .wav using timidity
        subprocess.run(['timidity', input_path, '-Ow', '-o', wav_output_path])

        # Convert .wav to .mp3 using FFmpeg
        subprocess.run(['ffmpeg', '-i', wav_output_path, '-acodec', 'libmp3lame', '-q:a', '2', mp3_output_path])

        # Remove temporary files
        os.remove(input_path)
        os.remove(wav_output_path)

        return redirect('/')
    else:
        return 'Invalid file format', 400

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()

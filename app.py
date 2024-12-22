import os
import subprocess
import time
from flask import Flask, request, render_template, redirect, send_from_directory, url_for

app = Flask(__name__)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('converted', filename, as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        format = request.form['format']
        
        # 保存パスの設定
        input_path = os.path.join('uploads', file.filename)
        output_path = os.path.join('converted', f"{os.path.splitext(file.filename)[0]}.{format}")
        
        # ファイルの保存
        file.save(input_path)
        
        # 変換の実行
        convert_file(input_path, output_path, format)
        
        # 変換後ページにリダイレクト
        return redirect(url_for('result', filename=f"{os.path.splitext(file.filename)[0]}.{format}"))
    
    return render_template('upload.html')

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

def convert_file(input_path, output_path, format):
    # コーデックの設定
    if format == 'mp4':
        codec = 'libx264'
        audio_codec = 'aac'
    elif format == 'mp3':
        codec = 'libmp3lame'
        audio_codec = 'libmp3lame'
    elif format == 'mov':
        codec = 'libx264'
        audio_codec = 'aac'
    elif format == 'avi':
        codec = 'libxvid'
        audio_codec = 'mp3'
    elif format == 'mkv':
        codec = 'libx264'
        audio_codec = 'aac'
    elif format == 'webm':
        codec = 'libvpx'
        audio_codec = 'libvorbis'
    elif format == 'flv':
        codec = 'flv'
        audio_codec = 'aac'
    else:
        raise ValueError("Unsupported format")
    
    ffmpeg_path = 'C:/Users/kouda/Documents/３年/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe'
    
    command = [
        ffmpeg_path,
        '-i', input_path,
        '-vcodec', codec,
        '-acodec', audio_codec,
        output_path
    ]
    
    start_time = time.time()
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    end_time = time.time()
    
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
    result.check_returncode()
    
    duration = end_time - start_time
    print(f"変換にかかった時間: {duration:.2f} 秒")

if __name__ == '__main__':
    app.run(debug=True)

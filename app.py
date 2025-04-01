from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Route to serve static audio files
@app.route('/som/<path:filename>')
def serve_audio(filename):
    return send_from_directory('som', filename)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
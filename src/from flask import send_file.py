from flask import send_file

@app.route('/logs/labeled_intrusions.json')
def get_labeled_logs():
    return send_file('../logs/labeled_intrusions.json')

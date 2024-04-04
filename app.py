import os
import sys
import sqlite3
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from displayControler import DisplayControler

UPLOAD_FOLDER = 'uploads'
ALLOWED_IMG_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_TEXT_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

display_controler = DisplayControler()

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row 
    return connection

def allowed_file(filename, extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in extensions


conn = get_db_connection()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file the browser submits and empty file without a file name
        if file.filename == '':
            print('No selected file')
            flash('No selected file')
            return redirect(request.url) 
        if file and allowed_file(file.filename, ALLOWED_IMG_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
    return 'File uploaded successfully'

@app.route('/highlights')
def highlights():
    conn = get_db_connection()
    highlights = conn.execute('SELECT * FROM highlights').fetchall()
    conn.close()
    return render_template('highlights.html', highlights=highlights)

@app.route('/test')
def test():
    print('test')
    app.logger.warn('test')
    print('test')
    return "Test Page"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
import os
from flask import Flask, render_template, flash, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_session.__init__ import Session
import sqlite3

UPLOAD_FOLDER = './static/images_added_by _the_user/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SESSION_TYPE = 'memcache'

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///keys.db'
db = SQLAlchemy(app)
sess = Session()

class Keys(db.Model):
    key_id = db.Column(db.String(200), primary_key=True)
    img_path = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

#Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

with app.app_context():
    db.create_all()

def get_db_connection():
    conn = sqlite3.connect('./instance/keys.db')
    conn.row_factory = sqlite3.Row
    return conn

#Routes
@app.route('/')
def main():
    return render_template('main.html')



@app.route('/SearchanImage')
def SearchanImage():
    return render_template('SearchanImage.html')

@app.route('/memory_Cache')
def memory_Cache():
    return render_template('memory_Cache.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/saveImgLFS', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['image']
        key_id = request.form.get('img_key')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)

            #Save key and img_path into db
            conn = get_db_connection()
            conn.execute('INSERT INTO keys (key_id, img_path) VALUES (?, ?)', (key_id, img_path))
            conn.commit()
            conn.close()
            # flash("User Updated Successfully!")
            return render_template('main.html')


        # return 'Please choose a photo'
        # return 'Please choose a file that is \'png\', \'jpg\' or \'jpeg\''
        # return 'Please enter a key for the photo'
        # return 'This photo has been stored before. If you are sure it\'s not, please rename the photo'
        # Key constraints

@app.route('/search', methods=['GET', 'POST'])
def search():
    key_id = request.form.get('img_key')
    img_path = Keys.query.filter_by(key_id=key_id).first().img_path
    return render_template('SearchanImage.html', user_image = img_path)
#if key is not found

@app.route('/displayAllKeys' , methods=['GET', 'POST'])
def getAllKey():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        sqlite_select_query = """SELECT key_id from Keys"""
        cur.execute(sqlite_select_query)
        records = cur.fetchall()
        records = list(*zip(*records))
        conn.commit()
        print("Printing each row in column key")
        for column in records:
            print(column)
        conn.close()
        return render_template('displayAllKeys.html', keys_list = records)
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
        return render_template('displayAllKeys.html')
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")

# Displays any errors
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.run(debug=True)


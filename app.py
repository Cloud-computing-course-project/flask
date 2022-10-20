#////////////////////////////////////////Tasks///////////////////////////////
#Complete put in memcache (look at replace policy) (Doaa)
#Add baraa function for key (baraa) Done
#Front end: edit memcache config list (look at schema) + get values from db and show in html (in specific time) (Dalia)
#Front end: Add select capacity - edit clear button style - Done (Baraa)
#Backend: save capacity choosen - save policy choosen (in db) (Baraa)
#Frontend: Tell user the defult policy is random - Default capacity 5MB (Doaa)
#Put real data in Database





import os
from flask import Flask, render_template, flash, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from sqlalchemy.sql import func
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_session.__init__ import Session
import sqlite3

UPLOAD_FOLDER = './static/images_added_by _the_user/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SESSION_TYPE = 'memcache'

global memcache
memcache = {}

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

class MemcacheConfig(db.Model):
    capacity_MB = db.Column(db.Integer(), primary_key=True)
    replace_policy = db.Column(db.String(200), nullable=False)
    items_num = db.Column(db.Integer(), nullable=False)
    items_size = db.Column(db.Integer(), nullable=False)
    request_num = db.Column(db.Integer(), nullable=False)
    hit_rate_percent = db.Column(db.Float(), nullable=False)
    miss_rate_percent = db.Column(db.Float(), nullable=False)


#Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

with app.app_context():
    db.create_all()

def get_db_connection():
    conn = sqlite3.connect('./instance/keys.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_mem_db_connection():
    conn = sqlite3.connect('./instance/memcache_config.db')
    conn.row_factory = sqlite3.Row
    return conn

#Memcache operations
def put_in_memcache(key, value):
    #Check capacity and policy
    memcache[key] = value

def get_from_memcache(key):
    return memcache.get(key)

def clear_memcache():
    memcache.clear()

def invalidateKey(key):
    del memcache[key]

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
        key_id = request.form.get('img_key').strip()
        conn = get_db_connection()

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)

            raw = Keys.query.filter_by(key_id=key_id).first()
            key_exists = raw is not None
            if key_exists:
                raw.img_path = img_path #update in Database
                db.session.commit()
                if get_from_memcache(key_id):
                    invalidateKey(key_id)
                put_in_memcache(key_id, img_path)
                flash("Key Updated Successfully!")
            else: 
                #Save key and img_path into db                
                if key_id == null or key_id == '':
                    flash("Please enter a key for the photo")
                else:
                    conn.execute('INSERT INTO keys (key_id, img_path) VALUES (?, ?)', (key_id, img_path))
                    put_in_memcache(key_id, img_path)
                    flash("Key Added Successfully!")
        else:
            flash("Please choose a photo that is \'png\', \'jpg\' or \'jpeg\'")

        conn.commit()
        conn.close()
        return render_template('main.html')

@app.route('/saveConfig', methods=['GET', 'POST'])
def UploadDateToMem():
    if request.method == 'POST':
        capacity = request.form('range')
        conn = get_mem_db_connection()
        conn.execute('INSERT INTO memcache_config (capacity_MB) VALUES (?)', (capacity))
        flash("Capacity Added Successfully!")
    else:
        flash("Error Added !")
    conn.commit()
    conn.close()
    return render_template('memory_Cache.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    key_id = request.form.get('img_key')
    #search in mem_cache
    img_path_from_memcache = get_from_memcache(key_id)
    if img_path_from_memcache:
        return render_template('SearchanImage.html', user_image = img_path_from_memcache)
    #Get from database  
    else:
        img_path = Keys.query.filter_by(key_id=key_id).first()
        if img_path:
            return render_template('SearchanImage.html', user_image = img_path.img_path)
        else:
            flash("Key is not found")
            return render_template('SearchanImage.html')


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

@app.route('/clear', methods=['POST'])
def clear():
    clear_memcache()
    return render_template('policy.html')


# Displays any errors
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.run(debug=False)

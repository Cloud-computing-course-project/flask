from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///key.db'
db = SQLAlchemy(app)

class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

#Routes
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/displayAllKeys')
def displayAllKeys():
    return render_template('displayAllKeys.html')

@app.route('/SearchanImage')
def SearchanImage():
    return render_template('SearchanImage.html')

@app.route('/memory_Cache')
def memory_Cache():
    return render_template('memory_Cache.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')


# Displays any errors
if __name__ == "__main__":
    app.run(debug=True)
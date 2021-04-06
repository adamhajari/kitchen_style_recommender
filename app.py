import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import utils

database_file = 'kitchenstyles.db'
conn_str = f'sqlite:///{database_file}'

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
db = SQLAlchemy(app)
db.create_all()

class UserImageFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    image_id = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'image_id'),)
    

class ImageAttributes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, nullable=False)
    attribute = db.Column(db.String(100), nullable=False)
    __table_args__ = (db.UniqueConstraint('image_id', 'attribute', name='image_attribute_uc'),)


@app.route('/')
def index():
    return "Kitchen Profiles"


@app.route('/feedback', methods=['POST'])
def feedback():
    feedback = UserImageFeedback(
        user_id=request.form.get('user_id'),
        image_id=request.form.get('image_id'),
        feedback=request.form.get('feedback')
    )
    db.session.add(feedback)
    db.session.commit()
    return 'OK'

@app.route('/attributes', methods=['POST'])
def attributes():
    feedback = ImageAttributes(
        image_id=request.form.get('image_id'),
        attribute=request.form.get('attribute'),
    )
    db.session.add(feedback)
    db.session.commit()
    return 'OK'

@app.route('/profile')
def profile():
    user_id = int(request.args.get('user_id'))
    user_profile, image_count = utils.get_user_style_profile(user_id)
    html = []
    for attribute, count in user_profile.items():
        html.append(f'{attribute}: {100.0 * count / image_count}%')

    return '<br>'.join(html)

if __name__ == "__main__":
    app.run(debug=True)

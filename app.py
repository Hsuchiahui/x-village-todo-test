from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# initialize
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('postgres://fpcptzbrqressv:209f2ef12f975eaa73b97d5f6bf0e1edadbe2eefcf704990a3f02b1452b380d7@ec2-54-235-160-57.compute-1.amazonaws.com:5432/d38c6otikvuskm')
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# models
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    cost = db.Column(db.Integer, nullable=True)
    check = db.Column(db.Boolean, nullable=True)

# views
@app.route("/")
def index():
    return render_template('index.html')


def str2bool(v):
  return v in ("true")

@app.route("/record", methods=['POST'])
def add_record():
    req_data = request.form
    name = req_data['name']
    cost = req_data['cost']
    record = Record(name = name, cost = cost)
    db.session.add(record)
    db.session.commit()
    return 'Create Succeeded', 200


@app.route("/record", methods=['GET'])
def get_records():
    records = Record.query.all()
    records_data = [
        {
            'id': record.id,
            'name': record.name,
            'cost': record.cost,
            'check':record.check 
        }
        for record in records
    ]
    print(records_data)
    return jsonify(records_data), 200


@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = Record.query.filter_by(id=record_id).first()
    record_data = {
        'id': record.id,
        'name': record.name,
        'cost': record.cost
    }
    return jsonify(record_data), 200


@app.route('/record/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    req_data = request.form
    record = Record.query.filter_by(id=record_id).first()
    if 'check' in req_data:
        record.check =str2bool(req_data['check'])
    else:     
        record.name = req_data['name']
        record.cost = req_data['cost']
    db.session.add(record)
    db.session.commit()
    return 'Update Succeeded', 200


@app.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    record = Record.query.filter_by(id=record_id).first()
    db.session.delete(record)
    db.session.commit()
    return 'Delete Succeeded', 200

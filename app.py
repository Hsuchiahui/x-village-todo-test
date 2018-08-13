from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# initialize
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# models
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    cost = db.Column(db.Integer, nullable=True)


# views
@app.route("/")
def hello():
    return "Hello World!"


@app.route("/name/")
def name():
    return "Hello Frank"


@app.route("/record", methods=['POST'])
def add_record():
    req_data = request.form
    name = req_data['name']
    cost = req_data['cost']
    record = Record(name='breakfast', cost=70)
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
            'cost': record.cost
        }
        for record in records
    ]
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


@app.route("/record", methods=["PUT"])
def update_record():
    records = Record.query.filter_by(name='breakfast')
    return 'Update Succeeded', 200


@app.route("/record", methods=["DELETE"])
def delete_record():
    first_record = Record.query.filter_by(name='breakfast').first()
    db.session.delete(first_record)
    db.session.commit()
    return 'Delete Succeeded', 200

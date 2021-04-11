import os.path
from config import app, db, ma, database_file, project_dir
from flask import jsonify, render_template, request

from enum import Enum
from marshmallow_enum import EnumField
from dateutil import parser

# TODO: Develop a independent python module
# TODO: Probably better to develop a Event Bus
import sys
sys.path.insert(1, f"{project_dir}/../services/")
from ServiceMapping import ClassServiceHandler
####


# Models
class PresenceEnum(Enum):
    present = "P"
    absent = "F"
    late = "A"
    unknown = "U"

class Classroom(db.Model):
    __tablename__ = "classroom"
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(256), nullable=False)
    student_id = db.Column(db.Integer(), nullable=False)
    classcode = db.Column(db.String(256), nullable=False)
    classname = db.Column(db.String(256), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    presence = db.Column(db.Enum(PresenceEnum),
                         nullable=False,
                         default=PresenceEnum.unknown)


class ClassroomSchema(ma.SQLAlchemyAutoSchema):
    presence = EnumField(PresenceEnum, by_value=True)
    class Meta:
        model = Classroom

classroom_schema = ClassroomSchema()
all_classroom_schema = ClassroomSchema(many = True)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/attendence/", methods=["POST"])
def take_attendence():
    classcode = request.form["classcode"]
    date = request.form["date"]

    _class = ClassServiceHandler(classcode=classcode).get()
    classname = _class.get('classname')
    students = _class.get('students')

    return render_template("attendence.html",
                           students=students,
                           date=date,
                           classcode=classcode,
                           classname=classname)


@app.route("/api/classroom/attendence", methods=["POST"])
def post_attendence():
    enum_presence = request.form["presence"]
    new_data = {
        "classcode" : request.form["classcode"],
        "classname" : request.form["classname"],
        "student_name" : request.form["student_name"],
        "student_id" : int(request.form["student_id"]),
        "date" : parser.parse(request.form["date"]),
        "presence" : PresenceEnum(enum_presence)
    }
    classroom = Classroom(**new_data)
    db.session.add(classroom)
    db.session.commit()
    return "OK"

@app.route("/api/classroom", methods=["GET"])
def classroom_list():
    result = Classroom.query.all()
    return jsonify(all_classroom_schema.dump(result))



if __name__ == "__main__":
    if not os.path.exists(database_file):
        db.create_all()
    app.run(host="0.0.0.0", port=12301, debug=True)

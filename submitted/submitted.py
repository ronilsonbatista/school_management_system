import os.path
from config import app, db, ma, database_file, project_dir
from flask import jsonify, render_template, request

from enum import Enum
from marshmallow_enum import EnumField
from dateutil import parser

import sys
sys.path.insert(1, f"{project_dir}/../services/")
from ServiceMapping import ClassServiceHandler


task_identifier = db.Table(
        "task_identifier",
        db.Column("classcode", db.String, db.ForeignKey("class.classcode")),
        db.Column("task_id", db.Integer, db.ForeignKey("task.id")))

class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer(),
                   primary_key=True)
    task = db.Column(db.String(256), nullable=False)
    classes = db.relationship("Class", secondary=task_identifier)


class Class(db.Model):
    __tablename__ = "class"
    classcode = db.Column(db.String(256),
                          primary_key=True,
                          unique=True)
    classname = db.Column(db.String(256), 
                          nullable=False)
    tasks = db.relationship("Task", secondary=task_identifier)


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        fields = ["task", "id"]


class AllClassesSchema(ma.SQLAlchemyAutoSchema):
    tasks = ma.Nested(TaskSchema, many=True)
    class Meta:
        model = Class
        fields = ["classname", "classcode", "tasks"]

all_classes_schema = AllClassesSchema(many = True)



@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/submitted/", methods=["POST"])
def take_submitted():
    classcode = request.form["classcode"]

    _class = ClassServiceHandler(classcode=classcode).get()
    classname = _class.get('classname')
    students = _class.get('students')

    
    return render_template("submitted.html",
                           students=students,
                           date=  "onnection",
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12304, debug=True)
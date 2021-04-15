import os.path
from config import app, db, ma, database_file, project_dir
from flask import jsonify, render_template, request
from dateutil import parser

import sys
sys.path.insert(1, f"{project_dir}/../services/")
from ServiceMapping import ClassServiceHandler
from ServiceMapping import TaskServiceHandler


class Submitted(db.Model):
    __tablename__ = "submitted_task_"
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(256), nullable=False)
    student_id = db.Column(db.Integer(), nullable=False)
    classcode = db.Column(db.String(256), nullable=False)
    classname = db.Column(db.String(256), nullable=False)
    task_id = db.Column(db.Integer(), nullable=False)
    task = db.Column(db.String(256), nullable=False)
    is_corrected = db.Column(db.Boolean, nullable=False)

class SubmittedSchema(ma.SQLAlchemyAutoSchema):
    submitted = ma.Nested(Submitted, many=True)
    class Meta:
        model = Submitted
        # fields = ["task"]

all_submitted_task_schema = SubmittedSchema(many = True)

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


@app.route("/api/class/submitted/code", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api/submitted/", methods=["POST"])
def take_submitted():
    classcode = request.form["classcode"]

    _task = TaskServiceHandler(classcode=classcode).get()
    task = _task.get('tasks')
    
    _class = ClassServiceHandler(classcode=classcode).get()
    classname = _class.get('classname')
    students = _class.get('students')

    return render_template("submitted.html",
                           students=students,
                           tasks =  task,
                           classcode=classcode,
                           classname=classname)


@app.route("/api/submitted/task", methods=["POST"])
def post_attendence():
    new_data = {
        "classcode" : request.form["classcode"],
        "classname" : request.form["classname"],
        "student_name" : request.form["student_name"],
        "student_id" : int(request.form["student_id"]),
        "task" : request.form["presence"],
        "task_id" : int(request.form["task_id"]),
        "is_corrected" : bool(False),
    }

    submitted = Submitted(**new_data)
    db.session.add(submitted)
    db.session.commit()
    return "OK"

@app.route("/api/submitted/list", methods=["GET"])
def submitted_list():
    result = Submitted.query.all()
    return jsonify(all_submitted_task_schema.dump(result))

if __name__ == "__main__":
    if not os.path.exists(database_file):
        db.create_all()
    app.run(host="0.0.0.0", port=12304, debug=True)
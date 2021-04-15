import os.path
from config import app, db, ma, database_file, project_dir
from flask import jsonify, render_template, request
from dateutil import parser

import sys
sys.path.insert(1, f"{project_dir}/../services/")
from ServiceMapping import SubmittedServiceHandler

class Grade(db.Model):
    __tablename__ = "grade"
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(256), nullable=False)
    test_grade = db.Column(db.Integer(), nullable=False)
    classcode = db.Column(db.String(256), nullable=False)
    classname = db.Column(db.String(256), nullable=False)
    task_id = db.Column(db.Integer(), nullable=False)
    task = db.Column(db.String(256), nullable=False)
    is_corrected = db.Column(db.Boolean, nullable=False)

class GradeSchema(ma.SQLAlchemyAutoSchema):
    grade = ma.Nested(Grade, many=True)
    class Meta:
        model = Grade

all_grade_task_schema = GradeSchema(many = True)

@app.route("/api/class/grade/code", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api/grade/", methods=["POST"])
def take_grade():
    _task = SubmittedServiceHandler().get()

    return render_template("grade.html",
                           students= _task )

@app.route("/api/submitted/test/grade", methods=["POST"])
def post_attendence():
    new_data = {
        "classcode" : request.form["classcode"],
        "classname" : request.form["classname"],
        "student_name" : request.form["student_name"],
        "task" : request.form["task"],
        "task_id" : int(request.form["task_id"]),
        "test_grade" : int(request.form["grade"]),
        "is_corrected" : bool(True)
    }

    grade = Grade(**new_data)
    db.session.add(grade)
    db.session.commit()
    return "OK"

@app.route("/api/grade/list", methods=["GET"])
def submitted_list():
    result = Grade.query.all()
    return jsonify(all_grade_task_schema.dump(result))

if __name__ == "__main__":
    if not os.path.exists(database_file):
        db.create_all()
    app.run(host="0.0.0.0", port=12305, debug=True)
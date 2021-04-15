import os.path
from config import app, db, ma, database_file, project_dir
from flask import jsonify, render_template, request
from dateutil import parser

import sys
sys.path.insert(1, f"{project_dir}/../services/")
from ServiceMapping import SubmittedServiceHandler



@app.route("/api/class/grade/code", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api/grade/", methods=["POST"])
def take_grade():
    classcode = request.form["classcode"]

    _task = SubmittedServiceHandler().get()
    # task = _task.get('student_name')

    return render_template("grade.html",
                           students= _task )

@app.route("/api/submitted/task", methods=["POST"])
def post_attendence():
    enum_presence = request.form["presence"]
    new_data = {
        "classcode" : request.form["classcode"],
        "classname" : request.form["classname"],
        "student_name" : request.form["student_name"],
        "student_id" : int(request.form["student_id"]),
        "task" : request.form["presence"],
        "is_corrected" : bool(False)

    }

    submitted = Submitted(**new_data)
    db.session.add(submitted)
    db.session.commit()
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12305, debug=True)
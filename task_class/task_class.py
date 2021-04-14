import os.path
from config import app, db, ma, database_file, project_dir
from flask import jsonify, render_template, request

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

        
class ClassSchema(ma.SQLAlchemyAutoSchema):
    tasks = ma.Nested(TaskSchema, many=True)
    class Meta:
        model = Class
        fields = ["classname", "classcode", "tasks"]

class_schema = ClassSchema()

@app.route("/api/tasks/<classcode>", methods=["GET"])
def class_detail(classcode):
    classes = Class.query.get(classcode)
    return class_schema.jsonify(classes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12303, debug=True)
from config import app, db, ma
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


class AllClassesSchema(ma.SQLAlchemyAutoSchema):
    tasks = ma.Nested(TaskSchema, many=True)
    class Meta:
        model = Class
        fields = ["classname", "classcode", "tasks"]

all_classes_schema = AllClassesSchema(many = True)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def class_list():
    classes = Class.query.all()
    schema = all_classes_schema.dump(classes)
    return jsonify(schema)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12303, debug=True)
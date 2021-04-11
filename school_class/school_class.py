from config import app, db, ma
from flask import jsonify

student_identifier = db.Table(
        "student_identifier",
        db.Column("classcode", db.String, db.ForeignKey("class.classcode")),
        db.Column("student_id", db.Integer, db.ForeignKey("student.id")))

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer(),
                   primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    classes = db.relationship("Class", secondary=student_identifier)


class Class(db.Model):
    __tablename__ = "class"
    classcode = db.Column(db.String(256),
                          primary_key=True,
                          unique=True)
    classname = db.Column(db.String(256), 
                          nullable=False)
    students = db.relationship("Student", secondary=student_identifier)


class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        fields = ["name", "id", "email"]


class ClassSchema(ma.SQLAlchemyAutoSchema):
    students = ma.Nested(StudentSchema, many=True)
    class Meta:
        model = Class
        fields = ["classname", "classcode", "students"]


class AllClassesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Class
        fields = ["classname", "classcode"]

class_schema = ClassSchema()
all_classes_schema = AllClassesSchema(many = True)


@app.route("/")
def home():
    return "Hello Turma!  TEST" 

@app.route("/api/class", methods=["GET"])
def class_list():
    classes = Class.query.all()
    schema = all_classes_schema.dump(classes)
    return jsonify(schema)


@app.route("/api/class/<classcode>", methods=["GET"])
def class_detail(classcode):
    classes = Class.query.get(classcode)
    return class_schema.jsonify(classes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12300, debug=True)

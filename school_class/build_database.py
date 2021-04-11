import os
from config import app, db, ma, database_name
from school_class import Student, Class

# Data to initialize database with
STUDENTS = [
    {'name': 'Albert Einsten', 'email': 'albert.einstein@al.infnet.edu.br'},
    {'name': 'Marie Curie', 'email': 'marie.curie@al.infnet.edu.br'},
    {'name': 'Nicolas Tesla', 'email': 'nicolas.tesla@al.infnet.edu.br'},
]

CLASSES = [
        {'classname': "Desenvolvimento de Software Ágil e Escalável com Microsserviços",
         'classcode': "21E1_1"}
]

if os.path.exists(database_name):
    os.remove(database_name)


db.create_all()

for _class in CLASSES:
    class_obj = Class(**_class)
    db.session.add(class_obj)

for student in STUDENTS:
    student_obj = Student(**student)
    student_obj.classes.append(class_obj)
    db.session.add(student_obj)

db.session.commit()

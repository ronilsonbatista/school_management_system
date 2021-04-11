import os
from config import app, db, ma, database_name
from task_class import Task, Class

# Data to initialize database with
TASK = [
    {'task': 'TESTE DE PERFORMANCE - TP1'},
    {'task': 'TESTE DE PERFORMANCE - TP2'},
    {'task': 'ASSESSMENT'},
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

for task in TASK:
    task_obj = Task(**task)
    task_obj.classes.append(class_obj)
    db.session.add(task_obj)

db.session.commit()

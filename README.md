# school_management_system

Implementing microservices linked to the school system contexts: Discipline (Students and Registrations), Class and Activities. 
Using python and Flask.

## Build project

Activating python

```bash
pip install -r requirements.txt
source env/bin/activate
```

Run service

```bash
python school_class/school_class.py
python classroom/classroom.py
python task_class/task_class.py
python submitted/submitted.py
python test_grade/test_grade.py
```

## Endpoints

Disciplines and Students

```bash
GET - http://localhost:12300
GET - http://localhost:12300/api/class  
GET - http://localhost:12300/api/class/<classcode>
```
Attendence

```bash
GET - http://localhost:12301/api/attendence/code
POST - http://localhost:12301/attendence/  
GET - http://localhost:12301/api/classroom
```

Activity Registration

```bash
Get - http://localhost:12303/api/tasks/<classcode>
```

Activity Submitted

```bash
GET - http://localhost:12304/api/class/submitted/code 
POST - http://localhost:12304/api/submitted/  
POST -  http://localhost:12304/api/submitted/task  
GET - http://localhost:12304/api/submitted/list 
```

Grade

```bash
GET -  http://localhost:12305/api/class/grade/code
POST - http://localhost:12305/api/grade/ 
POST - http://localhost:12305/api/submitted/test/grade 
GET - http://localhost:12305/api/grade/list 
```
## License
[MIT](https://choosealicense.com/licenses/mit/)

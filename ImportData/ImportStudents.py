import sqlite3
import sys
from os.path import dirname, abspath
sys.path.append(abspath(dirname(dirname(__file__))))
from Blueprints.Student import Student
import ZermeloMain as Zermelo

list_of_students = Zermelo.studentsindepartments(602)

print("Number of students: ", len(list_of_students))
# Create a connection to the database
conn = sqlite3.connect('./database.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS STUDENTS")
table = """ CREATE TABLE STUDENTS (
    id INTEGER PRIMARY KEY,
    student TEXT NOT NULL,
    departmentOfBranch INTEGER NOT NULL,
    mentorGroup INTEGER,
    mainGroup INTEGER NOT NULL,
    groupInDepartments TEXT,
    fullName TEXT NOT NULL,
    schoolInSchoolYear INTEGER NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    departmentOfBranchCode TEXT NOT NULL,
    mainGroupName TEXT NOT NULL,
    prefix TEXT
        ); """
c.execute(table)

for student in list_of_students:
    studentClass = Student(student)
    print(studentClass)
    c.execute("INSERT INTO STUDENTS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", studentClass.to_tuple())

conn.commit()
conn.close()
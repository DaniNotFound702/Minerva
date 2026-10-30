import sqlite3
import sys
from os.path import dirname, abspath
from time import sleep

sys.path.append(abspath(dirname(dirname(__file__))))
import ImportAppointments
import threading

done = False


def splitList(inputList, n):
    for i in range(0, len(inputList), n):
        yield inputList[i:i + n]

def importThread(inputStudents, start, end):
    for student in inputStudents:
        ImportAppointments.ImportAppointments(student[0])

def savingThread():
    while True:
        print("Waiting 30 seconds before saving")
        sleep(30)
        print("Committing")
        ImportAppointments.commit()
        print("Done saving")
        sleep(5)
        if done:
            break

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Please provide action") 
        sys.exit()
    action = args[1]
    if action == "allDatabase":
        conn = sqlite3.connect('./database.db')
        c = conn.cursor()
        student_table = c.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name LIKE 'STUDENTS_%'
            ORDER BY CAST(substr(name, 10) AS INTEGER) DESC
            LIMIT 1
        """).fetchone()
        if student_table is None:
            raise RuntimeError("No STUDENTS_<year-id> table found")

        table_name = student_table[0].replace('"', '""')
        c.execute(f'SELECT student FROM "{table_name}"')
        students = c.fetchall()
        ImportAppointments.setMass(True, student_table[0])
        numberOfThreads = 10
        lists = list(splitList(students, len(students) // numberOfThreads))
        if numberOfThreads > len(lists):
            numberOfThreads = len(lists)
        threads = []
        for i in range(numberOfThreads):
            threads.append(threading.Thread(target=importThread, args=(lists[i], 1, 52)))
            threads[i].start()
        saving = threading.Thread(target=savingThread)
        saving.start()
        # wait for threads to finish
        for i in range(numberOfThreads):
            threads[i].join()
        done = True
        saving.join()
        conn.close()
        ImportAppointments.commit()
        ImportAppointments.close()
    elif action == "students":
        # Range
        if len(args) < 4:
            print("Please provide student range")
            sys.exit()
        studentsStart = args[2]
        print("Importing appointments for students from: ", studentsStart)
        studentsEnd = args[3]
        print("Importing appointments for students to: ", studentsEnd)
        for i in range(int(studentsStart), int(studentsEnd) + 1):
            print("Importing appointments for: ", i)
            ImportAppointments.ImportAppointments(i)
        ImportAppointments.commit()
        ImportAppointments.close()



def close():
    ImportAppointments.commit()
    ImportAppointments.close()
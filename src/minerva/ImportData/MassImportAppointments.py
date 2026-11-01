import sqlite3
from time import sleep
from . import ImportAppointments
import threading
from os.path import exists


def splitList(inputList, n):
    for i in range(0, len(inputList), n):
        yield inputList[i:i + n]

def importThread(inputStudents, start, end, api_client, errors, stop_event):
    for student in inputStudents:
        if stop_event.is_set():
            return
        try:
            ImportAppointments.ImportAppointments(student[0], api_client=api_client)
        except Exception as error:
            errors.append(error)
            stop_event.set()
            return

def savingThread(stop_event):
    while not stop_event.wait(30):
        print("Committing")
        ImportAppointments.commit()
        print("Done saving")

def saveAll(database_path, api_client):
    conn = None
    stop_event = threading.Event()
    errors = []
    try:
        if not database_path:
            raise ValueError("Database path is not provided.")
        if not exists(database_path):
            raise FileNotFoundError(f"Database directory not found at {database_path}")
        conn = sqlite3.connect(f'{database_path}/database.db')
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
        if not students:
            raise RuntimeError(f"No students found in {student_table[0]}")
        ImportAppointments.setMass(True, student_table[0])
        numberOfThreads = min(10, len(students))
        chunk_size = (len(students) + numberOfThreads - 1) // numberOfThreads
        lists = list(splitList(students, chunk_size))
        threads = []
        for i in range(numberOfThreads):
            threads.append(threading.Thread(
                target=importThread,
                args=(lists[i], 1, 52, api_client, errors, stop_event),
            ))
            threads[i].start()
        saving = threading.Thread(target=savingThread, args=(stop_event,))
        saving.start()
        # wait for threads to finish
        for i in range(numberOfThreads):
            threads[i].join()
        stop_event.set()
        saving.join()
        if errors:
            raise RuntimeError(
                f"{len(errors)} appointment import(s) failed"
            ) from errors[0]
    finally:
        if conn is not None:
            conn.close()
        ImportAppointments.commit()
        ImportAppointments.close()


def saveRange(database_path, firstStudent, lastStudent):
    try:
        if not exists(database_path):
            raise FileNotFoundError(f"Database directory not found at {database_path}")
        if database_path is None:
            raise ValueError("Database path is not provided.")
        for student in range(int(firstStudent), int(lastStudent) + 1):
            ImportAppointments.ImportAppointments(student)
        ImportAppointments.commit()
        ImportAppointments.close()
    except Exception as e:
        print("Error occurred while saving appointments: ", e)
        ImportAppointments.commit()
        ImportAppointments.close()



def close():
    ImportAppointments.commit()
    ImportAppointments.close()
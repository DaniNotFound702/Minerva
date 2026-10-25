import datetime
import sqlite3
import sys
from os.path import dirname, abspath
sys.path.append(abspath(dirname(dirname(__file__))))
from Blueprints.Appointment import Appointment
import ZermeloMain as Zermelo
import threading
from helper.year import get_year_id
from helper.year import convert_id_to_year

# Create a connection to the database
appointmentConn = sqlite3.connect('./appointments.db', check_same_thread=False)
dbConn = sqlite3.connect('./database.db')
appointmentCursor = appointmentConn.cursor()
dbCursor = dbConn.cursor()

mass = False

massUsers = {}

lock = threading.Lock()

massAppointmentObjectList = {}




def makeSureTablesExist(week, year):
    table = f""" CREATE TABLE IF NOT EXISTS '{year}-{week}' (
            id INTEGER PRIMARY KEY,
            appointmentInstance TEXT,
            start INTEGER,
            end INTEGER,
            startTimeSlot INTEGER,
            endTimeSlot INTEGER,
            branch TEXT,
            type TEXT,
            groupsInDepartments TEXT,
            locationsOfBranch TEXT,
            optional BOOLEAN,
            valid BOOLEAN,
            cancelled BOOLEAN,
            cancelledReason TEXT,
            modified BOOLEAN,
            teacherChanged BOOLEAN,
            groupChanged BOOLEAN,
            locationChanged BOOLEAN,
            timeChanged BOOLEAN,
            moved BOOLEAN,
            created INTEGER,
            hidden BOOLEAN,
            changeDescription TEXT,
            schedulerRemark TEXT,
            content TEXT,
            lastModified INTEGER,
            new BOOLEAN,
            choosableInDepartments TEXT,
            choosableInDepartmentCodes TEXT,
            extraStudentSource TEXT,
            onlineLocationUrl TEXT,
            expectedStudentCount INTEGER,
            expectedStudentCountOnline INTEGER,
            udmUUID TEXT,
            creator TEXT,
            onlineStudents TEXT,
            appointmentLastModified INTEGER,
            remark TEXT,
            availableSpace INTEGER,
            subjects TEXT,
            teachers TEXT,
            onlineTeachers TEXT
        ); """
    appointmentCursor.execute(table)
    table = f""" CREATE TABLE IF NOT EXISTS EVERYTHING (
            id INTEGER PRIMARY KEY,
            appointmentInstance TEXT,
            start INTEGER,
            end INTEGER,
            startTimeSlot INTEGER,
            endTimeSlot INTEGER,
            branch TEXT,
            type TEXT,
            groupsInDepartments TEXT,
            locationsOfBranch TEXT,
            optional BOOLEAN,
            valid BOOLEAN,
            cancelled BOOLEAN,
            cancelledReason TEXT,
            modified BOOLEAN,
            teacherChanged BOOLEAN,
            groupChanged BOOLEAN,
            locationChanged BOOLEAN,
            timeChanged BOOLEAN,
            moved BOOLEAN,
            created INTEGER,
            hidden BOOLEAN,
            changeDescription TEXT,
            schedulerRemark TEXT,
            content TEXT,
            lastModified INTEGER,
            new BOOLEAN,
            choosableInDepartments TEXT,
            choosableInDepartmentCodes TEXT,
            extraStudentSource TEXT,
            onlineLocationUrl TEXT,
            expectedStudentCount INTEGER,
            expectedStudentCountOnline INTEGER,
            udmUUID TEXT,
            creator TEXT,
            onlineStudents TEXT,
            appointmentLastModified INTEGER,
            remark TEXT,
            availableSpace INTEGER,
            subjects TEXT,
            teachers TEXT,
            onlineTeachers TEXT
        ); """
    appointmentCursor.execute(table)


def setMass(value):
    global mass
    mass = value
    if value:
        global massUsers
        users = dbCursor.execute("SELECT student, departmentOfBranchCode FROM STUDENTS").fetchall()
        for user in users:
            if "1" in user[1]:
                massUsers[user[0]] = True
            else:
                massUsers[user[0]] = False

def saveAppointments(appointmentObjectList):
    for (year, week) in appointmentObjectList:
        makeSureTablesExist(week, year)
        # print("Table created for week: ", week)
        # print(appointmentObjectList[(year, week)])
        # print(type(appointmentObjectList[(year, week)]))
        # print(len(appointmentObjectList[(year, week)]))
        for appointmentObject in appointmentObjectList[(year, week)]:
            appointmentCursor.execute(f"INSERT OR REPLACE INTO '{year}-{week}' VALUES ({', '.join(['?'] * 42)})", appointmentObject.to_tuple())
            appointmentCursor.execute(f"INSERT OR REPLACE INTO EVERYTHING VALUES ({', '.join(['?'] * 42)})", appointmentObject.to_tuple())

def ImportAppointments(user):

    list_of_appointments = []
    try:
        startYear, endYear, year_id = get_year_id()    
        for year in range(startYear, endYear + 1):
            result = Zermelo.appointments(year_id[year], year, user)
            if result is None:
                print("No appointments returned for year: ", year)
                continue
            list_of_appointments.extend(result)
    except Exception as e:
            raise e
    print("Number of appointments: ", len(list_of_appointments))
    # Tables will now be per week, no longer per user
    # First, sort the appointments by week
    if not mass:
        appointmentObjectList = {}
        for appointment in list_of_appointments:
            appointmentObject = Appointment(appointment)
            # print(appointmentObject)
            year, week, _ = datetime.datetime.fromtimestamp(appointmentObject.start).isocalendar()
            # print("Week: ", week)
            key = (year, week)
            if key in appointmentObjectList: appointmentObjectList[key].append(appointmentObject)
            else: appointmentObjectList[key] = [appointmentObject]
            # print("Type: " + str(type(appointmentObjectList[key])))
        saveAppointments(appointmentObjectList)
        appointmentConn.commit()
    else:
        with lock:
            global massAppointmentObjectList
            for appointment in list_of_appointments:
                appointmentObject = Appointment(appointment)
                # print(appointmentObject)
                year, week, _ = datetime.datetime.fromtimestamp(appointmentObject.start).isocalendar()
                # print("Week: ", week)
                key = (year, week)
                if key in massAppointmentObjectList: massAppointmentObjectList[key].append(appointmentObject)
                else: massAppointmentObjectList[key] = [appointmentObject]
                # print("Type: " + str(type(massAppointmentObjectList[key])))

def commit():
    with lock:
        saveAppointments(massAppointmentObjectList)
        appointmentConn.commit()
        massAppointmentObjectList.clear()

def close():
    appointmentConn.close()
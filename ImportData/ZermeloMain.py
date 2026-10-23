import requests
from dotenv import load_dotenv
import sys
import datetime
import json
import logging
from os.path import dirname, abspath
import os
sys.path.append(abspath(dirname(dirname(__file__))))
import helper.log_api_message as log_api_message


log_api_message = log_api_message.log_api_message 
load_dotenv()
SCHOOL = os.getenv("SCHOOL")
SCHOOLYEAR = os.getenv("SCHOOLYEAR")
AUTHORIZATION = os.getenv("AUTHORIZATION")

base_url = "https://" + str(SCHOOL) + ".zportal.nl/api/3/"

HEADERS = {
    "Authorization": AUTHORIZATION
}

if not os.path.isdir("./logs"):
    os.mkdir("./logs")
if not os.path.isdir("./logs/messages"):
    os.mkdir("./logs/messages")
logging.basicConfig(filename="./logs/messages.log",
                    format='%(asctime)s %(levelname)s: %(message)s',
                    filemode='w')

def appointments(schoolYear_id, schoolYear, user_id):

    fields = (
        "id", "appointmentInstance", "start", "end", "startTimeSlot", "endTimeSlot",
        "branch", "type", "groupsInDepartments", "locationsOfBranch", "optional",
        "valid", "cancelled", "cancelledReason", "modified", "teacherChanged",
        "groupChanged", "locationChanged", "timeChanged", "moved", "created",
        "hidden", "changeDescription", "schedulerRemark", "content", "lastModified",
        "new", "choosableInDepartments", "choosableInDepartmentCodes",
        "extraStudentSource", "onlineLocationUrl", "expectedStudentCount",
        "expectedStudentCountOnline", "udmUUID", "creator", "onlineStudents",
        "appointmentLastModified", "remark", "availableSpace", "subjects",
        "teachers", "onlineTeachers", "availableSpace", "branch", "cancelledReason",
        "choosableInDepartments", "creator", "expectedStudentCount", 
        "expectedStudentCountOnline", "extraStudentSource", "groupsInDepartments",
        "locationsOfBranch", "modified", "moved", "new", "onlineLocationUrl", "onlineStudents", "onlineTeachers", "remark", "udmUUID"
    )
    # schooljaar `year` loopt van 1 aug `year` t/m 31 jul `year + 1`
    start = int(datetime.datetime(int(schoolYear), 8, 1).timestamp())
    end = int(datetime.datetime(int(schoolYear) + 1, 7, 31).timestamp())

    data = get_endpoint("appointments", "schoolInSchoolYear=" + str(schoolYear_id) + "&user=" + str(user_id) + "&start=" + str(start) + "&end=" + str(end) + "&fields=" + ",".join(fields))
    return data


def branchesofschools():
    fields = ("branch", "id", "schoolInSchoolYear", "name")
    data = get_endpoint("branchesofschools", "&fields=" + ",".join(fields))
    return data


def departmentsofbranches (): 
    fields = ("branchOfSchoolCode", "educationType", "educations", "mainGroupAuthority", "profiles", "schoolInSchoolYearId", "schoolInSchoolYearName", "teacherTeams", "teachingLevel", "weekTimeTable", "yearOfEducation")
    data = get_endpoint("departmentsofbranches", "fields=" + ",".join(fields))
    return data

def branches():
    fields = ("name", "code", "somCode", "somUuid")
    data = get_endpoint("branches", "fields=" + ",".join(fields))
    return data

def choosableindepartments():
    fields = ("courseType", "departmentOfBranchCode", "excludedSegments", "iltCode", "isExam", "lessonHoursInClassPeriods", "qualifiedCode", "scheduleCode", "scroungeSegments", "sectionOfBranch", "sectionOfBranchAbbreviation", "studentCanEdit", "subjectCode", "subjectName", "subjectScheduleCode", "subjectType")
    data = get_endpoint("choosableindepartments", "fields=" + ",".join(fields))
    return data

def groupindepartments():
    fields = ("id", "departmentOfBranch", "extendedName", "isMainGroup", "isMentorGroup", "name")
    data = get_endpoint("groupindepartments", "fields=" + ",".join(fields))
    return data

def holidays():
    fields = ("id", "start", "end", "schoolInSchoolYear", "name")
    data = get_endpoint("holidays", "fields=" + ",".join(fields))
    return data

def locationofbranches():
    fields = ("id", "student", "departmentOfBranch", "mentorGroup", "mainGroup", "groupInDepartments", "fullName", "schoolInSchoolYear", "firstName", "lastName", "departmentOfBranchCode", "mainGroupName", "prefix")
    data = get_endpoint("locationofbranches", "fields=" + ",".join(fields))
    return data


def schoolsinschoolyears(schoolYear):
    fields = ("archived", "archivedTime", "id", "name", "school","year", "branchOfSchools", "project", "projectName", "schoolHrmsCode", "schoolName")
    data = get_endpoint("schoolsinschoolyears","schoolInSchoolYear=" + str(schoolYear) + "&fields=" + ",".join(fields))
    return data

def timeslotnames(schoolYear):
    fields = ("code","id", "schoolInSchoolYear")
    data = get_endpoint("timeslotnames", "fields=" + ",".join(fields))
    return data

def studentsindepartments (schoolYear):
    fields = ("id","student","departmentOfBranch","mentorGroup","mainGroup","groupInDepartments","fullName","schoolInSchoolYear","firstName","lastName","departmentOfBranchCode","mainGroupName","prefix")
    data = get_endpoint("studentsindepartments", "schoolInSchoolYear=" + str("602") + "&fields=" + ",".join(fields))
    return data


def subjectselectionsubjects(schoolYear):
    fields = ("id","student","departmentOfBranch","mentorGroup","mainGroup","groupInDepartments","fullName","schoolInSchoolYear","firstName","lastName","departmentOfBranchCode","mainGroupName","prefix")
    data = get_endpoint("subjectselectionsubjects", "schoolInSchoolYear=" + str("602") + "&fields=" + ",".join(fields))
    return data

def get_endpoint(endpoint, parameters):
    url = f"{base_url}{endpoint}?{parameters}"
    try:
        req = requests.get(url, headers=HEADERS)
        
        json_data = req.json()
        # Logging the API request and response
        log_api_message(url, HEADERS, json_data)

        api_response = json_data.get("response", {})
        status = api_response.get("status")
        
        if status != 200:
            message = api_response.get("message", "Onbekende fout")
            logging.error(f"Fout in get_endpoint: {status} {message}")
            
            # 401 Unauthorized logica
            if status == 401:
                logging.info("Token verlopen. Nieuw token ophalen en opnieuw proberen...")
                get_api_token()
                logging.info("Nieuw token opgehaald. Probeer opnieuw. door opnieuw te starten.")
                quit()
            raise Exception(f"API Error {status}: {message}")
            
        return json_data["response"]["data"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Netwerk of HTTP fout in get_endpoint: {e}")
        raise
    except Exception as e:
        logging.error(f"Onverwachte fout in get_endpoint: {e}")
        raise



import requests
from dotenv import load_dotenv
import os
import datetime
import json
import logging


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

def appointments(schoolYear_id, schoolYear, user_id=21187):

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
    print("schoolYear_id: ", schoolYear_id)
    # schooljaar `year` loopt van 1 aug `year` t/m 31 jul `year + 1`
    start = int(datetime.datetime(int(schoolYear), 8, 1).timestamp())
    end = int(datetime.datetime(int(schoolYear) + 1, 7, 31).timestamp())

    data = get_endpoint("appointments", "schoolInSchoolYear=" + str(schoolYear_id) + "&user=" + str(user_id) + "&start=" + str(start) + "&end=" + str(end) + "&fields=" + ",".join(fields))
    print(data)
    return data


def branchesofschools(schoolYear_id):
    fields = ("branch", "id", "schoolInSchoolYear", "name")
    data = get_endpoint("branchesofschools", "&fields=" + ",".join(fields))
    return data


def departmentsofbranches (schoolYear_id): 
    fields = ("branchOfSchool", "code","id")
    data = get_endpoint("departmentsofbranches", "fields=" + ",".join(fields))
    return data

def branches(schoolYear_id):
    fields = ("name", "code", "somCode", "somUuid")
    data = get_endpoint("branches", "fields=" + ",".join(fields))
    return data

def choosableindepartments(schoolYear_id):
    fields = ("departmentOfBranch", "id", "subject")
    data = get_endpoint("choosableindepartments", "fields=" + ",".join(fields))
    return data

def groupindepartments(schoolYear_id):
    fields = ("id")
    data = get_endpoint("groupindepartments", "fields=" + fields)
    return data

def holidays(schoolYear):
    fields = ("id", "start", "end", "schoolInSchoolYear", "name")
    data = get_endpoint("holidays", "fields=" + ",".join(fields))
    return data

def jobs(schoolYear):
    fields = ("contract", "created", "durationManually", "employmentType", "end", "fte", "fteReal", "functionCategory", "id", "lastModified", "lastModifiedBy", "start")
    data = get_endpoint("jobs", "fields=" + ",".join(fields))
    return data

def locationofbranches(schoolYear):
    fields = ("branchOfSchool", "id", "name", "schoolInSchoolYear")
    data = get_endpoint("locationofbranches", "fields=" + ",".join(fields))
    return data

def schoolsinschoolyears(schoolYear):
    fields = ("archived", "archivedTime", "id", "name", "school","year")
    data = get_endpoint("schoolsinschoolyears","schoolInSchoolYear=" + str("602") + "&fields=" + ",".join(fields))
    return data

def timeslotnames(schoolYear):
    fields = ("code","id", "schoolInSchoolYear")
    data = get_endpoint("timeslotnames", "fields=" + ",".join(fields))
    return data

def studentsindepartments (schoolYear):
    fields = ("id","student","departmentOfBranch","mentorGroup","mainGroup","groupInDepartments","fullName","schoolInSchoolYear","firstName","lastName","departmentOfBranchCode","mainGroupName","prefix")
    data = get_endpoint("studentsindepartments", "schoolInSchoolYear=652&archived=true&fields=" + ",".join(fields))
    return data



#data = get_appointments()
#json_str = json.dumps(data, indent=4)
#with open("sample.json", "w") as f:
#    f.write(json_str)
def get_endpoint(endpoint, parameters):
    url = base_url + endpoint + "?" + parameters
    req = requests.get(url, headers=HEADERS)
    json_data = json.loads(req.text)
    messagefile = "./logs/messages/message" + datetime.datetime.now().strftime("-%Y%m%d-%H%M%S%f") + ".json"
    json_data["request"] = {
        "url": url,
        "headers": HEADERS
    }
    with open(messagefile, 'w', encoding='utf-8') as f:
        # noinspection PyTypeChecker
        json.dump(json_data, f, ensure_ascii=False, indent=4, sort_keys=True)
    response = json_data["response"]
    if response["status"] != 200:
        raise Exception(str(response["status"]) + response["message"])
    return response["data"]


print(branchesofschools(SCHOOLYEAR))



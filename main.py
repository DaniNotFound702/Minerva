import requests
from dotenv import load_dotenv
import os
import datetime
import json

load_dotenv()
SCHOOL = os.getenv("SCHOOL")
SCHOOLYEAR = os.getenv("SCHOOLYEAR")
AUTHORIZATION = os.getenv("AUTHORIZATION")

base_url = "https://" + str(SCHOOL) + ".zportal.nl/api/3/"

HEADERS = {
    "Authorization": AUTHORIZATION
}



def appointments(year=SCHOOLYEAR, school_year_id=SCHOOLYEAR):
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
        "teachers", "onlineTeachers",
    )

    print(f"Getting appointments for year {year} (id {school_year_id})...")

    # schooljaar `year` loopt van 1 aug `year` t/m 31 jul `year + 1`
    start = int(datetime.datetime(int("2026"), 8, 1).timestamp())
    end = int(datetime.datetime(int("2026") + 1, 7, 31).timestamp())

    req_par = (
        base_url
        + "appointments?schoolInSchoolYear=" + str(school_year_id)
        + "&user=---"
        + "&start=" + str(start)
        + "&end=" + str(end)
        + "&fields=" + ",".join(fields)
    )

    return req_par

print(appointments())


def branchesofschools():
    fields = ("branch", "id", "schoolInSchoolYear")
    req_par = base_url + "branchesofschools?fields=" + ",".join(fields)
    return req_par


def users():
    fields = ("code",)
    req_par = base_url + "users?schoolInSchoolYear=" + str(SCHOOLYEAR) + "&fields=" + ",".join(fields)
    return req_par


def departmentsofbranches (): 
    fields = ("branchOfSchool", "code","id", "schoolInSchoolYear")
    req_par = base_url + "departmentsofbranches?fields=" + ",".join(fields)
    return req_par


def branches():
    fields = ("name", "code", "somCode", "somUuid")
    req_par = base_url + "branches?fields=" + ",".join(fields)
    return req_par

def choosableindepartments():
    fields = ("departmentOfBranch", "id", "subject")
    req_par = base_url + "choosableindepartments?fields=" + ",".join(fields)
    return req_par



#data = get_appointments()
#json_str = json.dumps(data, indent=4)
#with open("sample.json", "w") as f:
#    f.write(json_str)
def request_data(endpoint):
    print(f"Requesting data from {endpoint}...")
    req = requests.get(endpoint, headers=HEADERS)
    req.raise_for_status()
    return req.json()["response"]["data"]

if __name__ == "__main__":
    urls = [
        appointments(),
        choosableindepartments(),
        branchesofschools(),
        users(),
        departmentsofbranches(),
        branches(),
    ]

    results = [request_data(url) for url in urls]

    with open(f"{SCHOOLYEAR}.json", "w") as f:
        json.dump(results, f, indent=4)
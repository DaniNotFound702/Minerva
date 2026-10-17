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


def get_year_id():
    fields = ("year", "id")

    req_par = base_url + "schoolsinschoolyears?fields=" + ",".join(fields)
    req = requests.get(req_par, headers=HEADERS)
    rows = req.json()["response"]["data"]

    year_id = {}
    for row in rows:
        year_id[row["year"]] = row["id"]

    startYear = rows[0]["year"]
    endYear = rows[-1]["year"]
    startYearId = year_id[startYear]
    endYearId = year_id[endYear]

    return startYearId, endYearId, startYear, endYear, year_id


def get_appointments():
    _, _, startYear, endYear, year_id = get_year_id()
    print(year_id)
    data = []

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

    for year, school_year_id in year_id.items():
        print(f"Getting appointments for year {year} (id {school_year_id})...")

        # schooljaar `year` loopt van 1 aug `year` t/m 31 jul `year + 1`
        start = int(datetime.datetime(int(year), 8, 1).timestamp())
        end = int(datetime.datetime(int(year) + 1, 7, 31).timestamp())

        req_par = (
            base_url + "appointments?schoolInSchoolYear=" + str(school_year_id)
            + "&user=21187"
            + "&start=" + str(start)
            + "&end=" + str(end)
            + "&fields=" + ",".join(fields)
        )

        try:
            req = requests.get(req_par, headers=HEADERS)
            if req.status_code != 200:
                print(f"Error fetching appointments for year {year}: {req.status_code} {req.text[:200]}")
                continue
            print(f"Successfully fetched appointments for year {year}.")
            data.extend(req.json()["response"]["data"])
        except Exception as e:
            print(f"Error fetching appointments for year {year}: {e}")
            continue

    return data


def get_users():
    fields = ("code",)

    req_par = base_url + "users?schoolInSchoolYear=" + str(SCHOOLYEAR) + "&fields=" + ",".join(fields)
    req = requests.get(req_par, headers=HEADERS)
    print(req.json()["response"]["data"])


data = get_appointments()
json_str = json.dumps(data, indent=4)
with open("sample.json", "w") as f:
    f.write(json_str)


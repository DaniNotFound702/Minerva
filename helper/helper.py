import requests
from dotenv import load_dotenv
import os
from ImportData.ZermeloMain import get_endpoint

load_dotenv()
SCHOOL = os.getenv("SCHOOL")
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

def convert_year_to_id(year):
    fields = ("archived", "archivedTime", "id", "name", "school","year")
    data = get_endpoint("schoolsinschoolyears","schoolInSchoolYear=" + str(year) + "&fields=" + ",".join(fields))
    return data

def convert_id_to_year(id):
    fields = ("archived", "archivedTime", "id", "name", "school","year")
    data = get_endpoint("schoolsinschoolyears","id=" + str(id) + "&fields=" + ",".join(fields))
    return data[0]['year']


print(convert_year_to_id(2026))

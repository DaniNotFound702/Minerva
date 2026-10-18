import requests
from dotenv import load_dotenv
import os


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

get_year_id()
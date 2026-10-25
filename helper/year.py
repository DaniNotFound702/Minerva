import requests
from dotenv import load_dotenv
from os import getenv
import sys
from os.path import dirname, abspath
sys.path.append(abspath(dirname(dirname(__file__))))
from helper.api import get_endpoint

load_dotenv()
AUTHORIZATION = getenv("AUTHORIZATION")
SCHOOL = getenv("SCHOOL")
base_url = "https://" + str(SCHOOL) + ".zportal.nl/api/3/"
HEADERS = {
    "Authorization": AUTHORIZATION
}

def get_year_id():
    fields = ("year", "id")

    data = get_endpoint("schoolsinschoolyears", "fields=" + ",".join(fields))
    rows = data
    year_id = {}
    for row in rows:
        year_id[row["year"]] = row["id"]

    startYear = rows[0]["year"]
    endYear = rows[-1]["year"]

    return startYear, endYear, year_id
 
def convert_id_to_year(id):
    fields = ("archived", "archivedTime", "id", "name", "school","year")
    data = get_endpoint("schoolsinschoolyears","id=" + str(id) + "&fields=" + ",".join(fields))
    return data[0]['year']
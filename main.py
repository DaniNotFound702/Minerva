import requests
from dotenv import load_dotenv
import os


load_dotenv()
SCHOOL = os.getenv("SCHOOL")
SCHOOLYEAR = os.getenv("SCHOOLYEAR")
AUTHORIZATION = os.getenv("AUTHORIZATION")

base_url = "https://" + str(SCHOOL) + ".zportal.nl/api/3/"

HEADERS = {
    "Authorization": AUTHORIZATION
}

def get_test():
    req = base_url+ "groupindepartments?schoolInSchoolYear=652&fields=id,name,extendedName,departmentOfBranch"
    test2 = requests.get(req, headers=HEADERS)
    print(test2)

get_test()
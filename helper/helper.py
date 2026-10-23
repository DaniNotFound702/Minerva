import requests
from dotenv import load_dotenv
import os
import datetime
import time
from selenium import webdriver
from datetime import datetime
import sys 
from os.path import dirname, abspath
sys.path.append(abspath(dirname(dirname(__file__))))
from ImportData.ZermeloMain import get_endpoint


load_dotenv()
AUTHORIZATION = os.getenv("AUTHORIZATION")
SCHOOL = os.getenv("SCHOOL")
base_url = "https://" + str(SCHOOL) + ".zportal.nl/api/3/"
HEADERS = {
    "Authorization": AUTHORIZATION
}


def convert_year_to_id(year):
    fields = ("archived", "archivedTime", "id", "name", "school","year")
    data = get_endpoint("schoolsinschoolyears","schoolInSchoolYear=" + str(year) + "&fields=" + ",".join(fields))
    return data

def convert_id_to_year(id):
    fields = ("archived", "archivedTime", "id", "name", "school","year")
    data = get_endpoint("schoolsinschoolyears","id=" + str(id) + "&fields=" + ",".join(fields))
    return data[0]['year']

convert_id_to_year(602)
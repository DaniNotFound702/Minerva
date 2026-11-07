import os

from dotenv import load_dotenv
from minerva import ZermeloAPIClient, ZermeloMain

load_dotenv()

client = ZermeloAPIClient(
	school=os.environ["SCHOOL"],
	authorization=os.environ["AUTHORIZATION"],
)
zermelo = ZermeloMain(client)

branches = zermelo.branches()
holidays = zermelo.holidays()
students = zermelo.studentsindepartments(schoolYear=1234)
appointments = zermelo.appointments(
	schoolYear_id=652,
	schoolYear=2026,
	user_id="1234567890",
)

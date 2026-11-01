
from minerva.ImportData.ZermeloMain import ZermeloMain
from minerva.helper.api import ZermeloAPIClient

client = ZermeloAPIClient(
	school="",
	authorization="Bearer ",
)
zermelo = ZermeloMain(client)

branches = zermelo.branches()
holidays = zermelo.holidays()
students = zermelo.studentsindepartments(schoolYear=1234)


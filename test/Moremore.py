from minerva import ZermeloAPIClient, ZermeloMain

client = ZermeloAPIClient(
    school="csghetstreek",
    authorization="Bearer 3nf2epkefnj64in6itacq9tk04",
)
zermelo = ZermeloMain(client)

branches = zermelo.branches()
holidays = zermelo.holidays()
students = zermelo.studentsindepartments(schoolYear=1234)
appointments = zermelo.appointments(
	schoolYear_id=652,
	schoolYear=2026,
	user_id=21187,
)
